import asyncio
import random
import time

import requests

from receiver.schemas import LocationSchema, QuoteSchema

BASE_PRICE = 100
KILOMETER_PRICE = 25
MINUTE_PRICE = 5
PROVIDER_NAME = "mock"


class MockProvider:
    def __init__(self):
        self.url = "https://router.project-osrm.org/route/v1/driving/"
        self.params = {
            "overview": "false",
        }

    def calculate_demand_and_jams(self):
        demand = round(random.uniform(1, 2), 1)
        jams = round(random.uniform(1, 2), 1)
        return demand, jams

    async def calculate_quote(
        self, origin: LocationSchema, destination: LocationSchema
    ) -> QuoteSchema:
        return await asyncio.to_thread(
            self._calculate_quote_sync, origin, destination
        )

    def _calculate_quote_sync(
        self, origin: LocationSchema, destination: LocationSchema
    ) -> QuoteSchema:
        url = (
            f"{self.url}{origin.latitude},{origin.longitude};"
            f"{destination.latitude},{destination.longitude}"
        )

        response = requests.get(url, params=self.params, timeout=30)
        response.raise_for_status()
        data = response.json()

        time.sleep(3)

        route = data["routes"][0]

        distance_km = route["distance"] / 1000
        duration_minutes = route["duration"] / 60

        demand, jams = self.calculate_demand_and_jams()

        price = (
            BASE_PRICE
            + (distance_km * KILOMETER_PRICE)
            + (duration_minutes * MINUTE_PRICE)
        ) * demand * jams

        return QuoteSchema(
            provider=PROVIDER_NAME,
            price=round(price, 2),
            duration=int(round(duration_minutes)),
            distance=round(distance_km, 2),
        )
