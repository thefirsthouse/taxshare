from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from receiver.service import SearchService
from quotes.quote_collector import QuoteCollector

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_search_service(session: SessionDep) -> SearchService:
    return SearchService(session)

SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]


def get_quote_collector() -> QuoteCollector:
    return QuoteCollector()

QuoteCollectorDep = Annotated[QuoteCollector, Depends(get_quote_collector)]
