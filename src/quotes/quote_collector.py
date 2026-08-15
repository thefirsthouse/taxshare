import asyncio
from collections.abc import AsyncIterator

import httpx

from quotes.providers.mock import MockProvider
from receiver.schemas import LocationSchema, QuoteSchema


class QuoteCollector:
    def __init__(self, client: httpx.AsyncClient):
        self.providers = [
            MockProvider(client),
        ]

    async def collect_quotes(
        self, origin: LocationSchema, destination: LocationSchema
    ) -> AsyncIterator[QuoteSchema]:
        tasks = [
            asyncio.create_task(provider.calculate_quote(origin, destination))
            for provider in self.providers
        ]

        for task in asyncio.as_completed(tasks):
            yield await task
