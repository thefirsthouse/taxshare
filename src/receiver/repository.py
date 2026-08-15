from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from receiver.models import SearchModel


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, search_id: int) -> SearchModel | None:
        result = await self._session.execute(
            select(SearchModel).where(SearchModel.id == search_id)
        )
        return result.scalar_one_or_none()

    async def create_search(self, search: SearchModel):
        self._session.add(search)
        await self._session.commit()
        await self._session.refresh(search)
        return search

    async def update_search(self, search: SearchModel):
        self._session.add(search)
        await self._session.commit()
        await self._session.refresh(search)
        return search
