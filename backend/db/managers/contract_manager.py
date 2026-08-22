from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.contracts import Contract, ContractStatus


class ContractManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_release(self, release_id: int) -> Contract | None:
        stmt = select(Contract).where(Contract.release_id == release_id)
        return await self.session.scalar(stmt)

    async def get_by_id(self, contract_id: int) -> Contract | None:
        stmt = select(Contract).where(Contract.id == contract_id)
        return await self.session.scalar(stmt)

    async def create_for_release(
        self,
        release_id: int,
        version: str = "v0.3",
        file_url: str | None = None,
    ) -> Contract:
        existing = await self.get_by_release(release_id)
        if existing:
            return existing
        contract = Contract(
            release_id=release_id,
            status=ContractStatus.UNSIGNED,
            version=version,
            file_url=file_url,
        )
        self.session.add(contract)
        await self.session.commit()
        await self.session.refresh(contract)
        return contract

    async def sign(
        self,
        contract: Contract,
        artist_full_name: str,
        file_url: str | None = None,
    ) -> Contract:
        contract.status = ContractStatus.SIGNED
        contract.artist_full_name = artist_full_name
        contract.signed_at = datetime.now(timezone.utc)
        if file_url:
            contract.file_url = file_url
        await self.session.commit()
        await self.session.refresh(contract)
        return contract

    async def mark_needs_resign(self, contract: Contract) -> Contract:
        contract.status = ContractStatus.NEEDS_RESIGN
        contract.signed_at = None
        await self.session.commit()
        await self.session.refresh(contract)
        return contract

    async def void(self, contract: Contract) -> Contract:
        contract.status = ContractStatus.VOID
        await self.session.commit()
        await self.session.refresh(contract)
        return contract
