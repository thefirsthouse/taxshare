from typing import Annotated

import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from receiver.service import SearchService
from quotes.quote_collector import QuoteCollector

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_search_service(session: SessionDep) -> SearchService:
    return SearchService(session)

SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]


def get_quote_collector(request: Request) -> QuoteCollector:
    client: httpx.AsyncClient = request.app.state.http_client
    return QuoteCollector(client)

QuoteCollectorDep = Annotated[QuoteCollector, Depends(get_quote_collector)]
