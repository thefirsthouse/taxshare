from typing import List

from fastapi import APIRouter

from receiver.service import SearchService
from receiver.schemas import SearchRequest, SearchResponse
from receiver.dependencies import SearchServiceDep
from database import get_session

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/search", response_model=SearchResponse)
async def create_search(
    search: SearchRequest,
    session: SearchServiceDep,
):
    return await session.create_search(search)
