from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from receiver.models import SearchModel
from receiver.schemas import SearchRequest
from receiver.repository import SearchRepository

class SearchService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = SearchRepository(session)
    
    async def create_search(self, search: SearchRequest) -> SearchModel:
        search_model = SearchModel(
            start_location=search.start_location.model_dump(),
            end_location=search.end_location.model_dump(),
            created_at=search.created_at,
            quotes=[],
        )
        await self._repository.create_search(search_model)
        return search_model
