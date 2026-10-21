from fastapi import APIRouter, Depends, Query
from pymongo.asynchronous.database import AsyncDatabase

from backend.database.mongodb import get_database
from backend.repositories.poi_repository import POIRepository
from backend.schemas.poi import AnimalCatalogResponse, POIResponse

router = APIRouter(prefix="/api/pois", tags=["pois"])


def get_poi_repository() -> POIRepository:
    database: AsyncDatabase = get_database()
    return POIRepository(database)


@router.get("", response_model=list[POIResponse])
async def list_pois(
    language: str = Query(..., min_length=1),
    repository: POIRepository = Depends(get_poi_repository),
) -> list[POIResponse]:
    return await repository.list_for_language(language)


@router.get("/catalog", response_model=list[AnimalCatalogResponse])
async def list_animal_catalog(
    language: str = Query(..., min_length=1),
    repository: POIRepository = Depends(get_poi_repository),
) -> list[AnimalCatalogResponse]:
    return await repository.list_animal_catalog(language)
