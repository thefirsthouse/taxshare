import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from receiver.models import SearchModel
from receiver.repository import SearchRepository
from receiver.schemas import LocationSchema, QuoteSchema, SearchRequest, SearchResponse


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

    async def get_search(self, search_id: int) -> SearchModel:
        search_model = await self._repository.get_by_id(search_id)
        if search_model is None:
            raise ValueError(f"Search {search_id} not found")
        return search_model

    async def add_quote(self, search_id: int, quote: QuoteSchema) -> SearchModel:
        search_model = await self.get_search(search_id)

        quotes = list(search_model.quotes or [])
        quotes.append(quote.model_dump())
        search_model.quotes = quotes
        search_model.updated_at = datetime.datetime.now()
        return await self._repository.update_search(search_model)

    @staticmethod
    def to_response(search_model: SearchModel) -> SearchResponse:
        return SearchResponse(
            id=search_model.id,
            start_location=LocationSchema.model_validate(search_model.start_location),
            end_location=LocationSchema.model_validate(search_model.end_location),
            quotes=[
                QuoteSchema.model_validate(quote)
                for quote in (search_model.quotes or [])
            ],
            created_at=search_model.created_at,
            updated_at=search_model.updated_at,
        )
