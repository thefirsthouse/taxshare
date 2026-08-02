from operator import ge
from typing import List
import datetime
from sqlalchemy import DateTime, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from receiver.schemas import LocationSchema, QuoteSchema


class SearchModel(Base):
    __tablename__ = "searches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_location: Mapped[LocationSchema] = mapped_column(JSON)
    end_location: Mapped[LocationSchema] = mapped_column(JSON)
    distance: Mapped[float | None] = mapped_column(Float)
    duration: Mapped[int | None] = mapped_column(Integer)
    quotes: Mapped[List[QuoteSchema]] = mapped_column(JSON)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return f"SearchModel(id={self.id}, start_location={self.start_location}, end_location={self.end_location}, distance={self.distance}, duration={self.duration}, quotes={self.quotes}, created_at={self.created_at}, updated_at={self.updated_at})"

    def to_dict(self):
        return {
            "id": self.id,
            "start_location": self.start_location,
            "end_location": self.end_location,
            "distance": self.distance,
            "duration": self.duration,
        }

    def from_dict(self, data):
        self.start_location = data["start_location"]
        self.end_location = data["end_location"]
        self.distance = data["distance"]
        self.duration = data["duration"]
        self.quotes = data["quotes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
