import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from quotes.quote_collector import QuoteCollector
from receiver.dependencies import QuoteCollectorDep, SearchServiceDep
from receiver.schemas import SearchRequest
from receiver.service import SearchService

router = APIRouter()


def _format_sse(response) -> str:
    return f"data: {json.dumps(response.model_dump(mode='json'))}\n\n"


async def _stream_search_updates(
    search_service: SearchService,
    quote_collector: QuoteCollector,
    search: SearchRequest,
    search_id: int,
):
    search_model = await search_service.get_search(search_id)
    yield _format_sse(SearchService.to_response(search_model))

    async for quote in quote_collector.collect_quotes(
        search.start_location, search.end_location
    ):
        search_model = await search_service.add_quote(search_id, quote)
        yield _format_sse(SearchService.to_response(search_model))


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/search")
async def create_search(
    search: SearchRequest,
    session: SearchServiceDep,
    quote_collector: QuoteCollectorDep,
):
    search_model = await session.create_search(search)

    return StreamingResponse(
        _stream_search_updates(
            session, quote_collector, search, search_model.id
        ),
        media_type="text/event-stream",
    )
