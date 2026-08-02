from sqlalchemy.ext.asyncio import AsyncSession

from receiver.models import SearchModel


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create_search(self, search: SearchModel):
        self._session.add(search)
        await self._session.commit()
        await self._session.refresh(search)
        return search
