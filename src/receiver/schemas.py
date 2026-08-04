import datetime
from pydantic import BaseModel


class LocationSchema(BaseModel):
    latitude: float
    longitude: float
    address: str


class QuoteSchema(BaseModel):
    provider: str
    price: float
    duration: int
    distance: float


class SearchResponse(BaseModel):
    id: int
    start_location: LocationSchema
    end_location: LocationSchema
    quotes: List[QuoteSchema]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    start_location: LocationSchema
    end_location: LocationSchema
    created_at: datetime.datetime = datetime.datetime.now()

    class Config:
        from_attributes = True
