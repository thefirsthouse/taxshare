from contextlib import asynccontextmanager
import httpx
import uvicorn
from fastapi import FastAPI

from config import settings
from database import engine, Base
from receiver.router import router as receiver_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=30.0) as client:
        app.state.http_client = client

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        yield
    
    await engine.dispose()

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    debug=settings.debug,
    docs_url="/docs" if settings.app_env == "development" else None,
    lifespan=lifespan,
)

app.include_router(receiver_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
