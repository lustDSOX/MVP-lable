"""Storage backend: local disk or S3 (env STORAGE_BACKEND=local|s3)."""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import BinaryIO, Protocol


class StorageBackend(Protocol):
    def save(self, data: BinaryIO, key: str, content_type: str | None = None) -> str:
        ...

    def delete(self, key: str) -> None: ...


class LocalStorage:
    def __init__(self, root: str | Path, public_prefix: str = "/uploads"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.public_prefix = public_prefix.rstrip("/")

    def save(self, data: BinaryIO, key: str, content_type: str | None = None) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            while chunk := data.read(1024 * 1024):
                f.write(chunk)
        return f"{self.public_prefix}/{key}"

    def delete(self, key: str) -> None:
        path = self.root / key
        path.unlink(missing_ok=True)


class S3Storage:
    def __init__(
        self,
        bucket: str,
        region: str | None = None,
        endpoint_url: str | None = None,
        public_base: str | None = None,
    ):
        try:
            import boto3
        except ImportError as e:
            raise RuntimeError("boto3 required for S3 storage: pip install boto3") from e
        self.bucket = bucket
        self.public_base = (public_base or f"https://{bucket}.s3.amazonaws.com").rstrip("/")
        self.client = boto3.client(
            "s3",
            region_name=region or os.getenv("AWS_REGION"),
            endpoint_url=endpoint_url or os.getenv("S3_ENDPOINT_URL") or None,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def save(self, data: BinaryIO, key: str, content_type: str | None = None) -> str:
        extra = {}
        if content_type:
            extra["ContentType"] = content_type
        self.client.upload_fileobj(data, self.bucket, key, ExtraArgs=extra or None)
        return f"{self.public_base}/{key}"

    def delete(self, key: str) -> None:
        self.client.delete_object(Bucket=self.bucket, Key=key)


def get_storage() -> StorageBackend:
    backend = os.getenv("STORAGE_BACKEND", "local").lower()
    if backend == "s3":
        bucket = os.getenv("S3_BUCKET")
        if not bucket:
            raise RuntimeError("S3_BUCKET required when STORAGE_BACKEND=s3")
        return S3Storage(
            bucket=bucket,
            region=os.getenv("AWS_REGION"),
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            public_base=os.getenv("S3_PUBLIC_BASE"),
        )
    root = os.getenv("UPLOAD_DIR", "/tmp/label_uploads")
    return LocalStorage(root)


def make_key(subdir: str, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return f"{subdir}/{uuid.uuid4().hex}{ext}"
