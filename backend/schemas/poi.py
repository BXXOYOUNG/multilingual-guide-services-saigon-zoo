from pydantic import BaseModel


class POIResponse(BaseModel):
    id: str
    name: str
    description: str
    latitude: float
    longitude: float
