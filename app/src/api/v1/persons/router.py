from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from services import FilmService, PersonService
from core.auth import security_jwt
from api.v1.dependencies import get_pagination_params, get_search_query_by_name
from ..films.schemas import ShortenedFilm
from .schemas import DetailedPerson

router = APIRouter()


@router.get(
    "/{person_id}",
    description="Returns information about a specific person by ID",
    dependencies=[Depends(security_jwt)]
)
async def person_details(
    person_id: UUID = Path(...),
    person_service: PersonService = Depends(PersonService.get_instance),
) -> DetailedPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get(
    "/",
    description="Returns a list persons",
    dependencies=[Depends(security_jwt)]
)
async def person_list(
    search: dict = Depends(get_search_query_by_name),
    pagination_params: dict = Depends(get_pagination_params),
    person_service: PersonService = Depends(PersonService.get_instance),
) -> list[DetailedPerson]:
    persons = await person_service.get_many(search, pagination_params)
    return persons


@router.get(
    "/{person_id}/films",
    summary="Films by person ID",
    description="Returns a list of films for a specific person by ID",
    dependencies=[Depends(security_jwt)]
)
async def person_films(
    person_id: UUID = Path(...),
    person_service: PersonService = Depends(PersonService.get_instance),
    film_service: FilmService = Depends(FilmService.get_instance),
    pagination_params: dict = Depends(get_pagination_params),
) -> list[ShortenedFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    films = await film_service.get_films_by_person(person_id, pagination_params)
    return films
