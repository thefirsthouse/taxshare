import uvicorn
from fastapi import FastAPI

from config import settings
from database import engine, Base
from receiver.router import router as receiver_router

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    debug=settings.debug,
    docs_url="/docs" if settings.app_env == "development" else None,
)

app.include_router(receiver_router)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
