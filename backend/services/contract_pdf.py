"""Generate minimal valid PDF contract (no external deps)."""

from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO

from services.storage import get_storage, make_key


def _escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_pdf(lines: list[str]) -> bytes:
    content_parts = ["BT", "/F1 11 Tf", "50 780 Td", "14 TL"]
    first = True
    for line in lines:
        safe = _escape(line[:110])
        if first:
            content_parts.append(f"({safe}) Tj")
            first = False
        else:
            content_parts.append("T*")
            content_parts.append(f"({safe}) Tj")
    content_parts.append("ET")
    stream = "\n".join(content_parts)
    stream_bytes = stream.encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    objects.append(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    objects.append(
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n"
    )
    objects.append(
        f"4 0 obj<< /Length {len(stream_bytes)} >>stream\n".encode()
        + stream_bytes
        + b"\nendstream\nendobj\n"
    )
    objects.append(b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n")

    out = BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(out.tell())
        out.write(obj)
    xref_pos = out.tell()
    out.write(f"xref\n0 {len(objects) + 1}\n".encode())
    out.write(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.write(f"{off:010d} 00000 n \n".encode())
    out.write(
        f"trailer<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    )
    return out.getvalue()


def generate_contract_pdf(
    release_id: int,
    release_title: str,
    artist_full_name: str,
    version: str = "v0.3",
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"CLASS TICKETS / LABEL CONTRACT {version}",
        "=" * 48,
        f"Release ID: {release_id}",
        f"Title: {release_title}",
        f"Artist: {artist_full_name}",
        f"Generated: {now}",
        "",
        "1. Parties. Artist grants Label exclusive distribution rights",
        "   for the Release listed above for the Territory (Worldwide).",
        "2. Term. 3 (three) years from the Release Date, auto-renewing",
        "   for 1-year periods unless terminated with 90 days notice.",
        "3. Revenue share. Net receipts split 70% Artist / 30% Label",
        "   after distribution and payment-processing costs.",
        "4. Deliverables. Master audio, cover art (min 3000x3000),",
        "   metadata and lyrics as submitted in the Artist Cabinet.",
        "5. Moral rights. Artist warrants originality and clearance",
        "   of samples; indemnifies Label against third-party claims.",
        "",
        "Signature of Artist (electronic acceptance in Cabinet)",
        f"Name: {artist_full_name}",
        f"Date: {now}",
        "",
        "This PDF is generated for MVP demo purposes.",
    ]
    pdf_bytes = _build_pdf(lines)
    storage = get_storage()
    key = make_key("docs", f"contract_r{release_id}.pdf")
    return storage.save(BytesIO(pdf_bytes), key, content_type="application/pdf")
