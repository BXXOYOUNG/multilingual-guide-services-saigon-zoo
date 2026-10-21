from pydantic import BaseModel
from typing import Optional


class POIResponse(BaseModel):
    id: str
    name: str
    description: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    image_source_url: Optional[str] = None
    source_url: Optional[str] = None
    coordinate_source_url: Optional[str] = None
    coordinate_status: Optional[str] = None
    translation_review_status: Optional[str] = None


class AnimalCatalogResponse(BaseModel):
    id: str
    candidate_code: str
    scientific_name: str
    name: str
    description: str
    source_url: str
    map_available: bool
    image_url: Optional[str] = None
    image_source_url: Optional[str] = None
