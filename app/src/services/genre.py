import datetime as dt
from typing import ClassVar, Type

from pydantic import BaseModel

from models import Genre

from .base import BaseService


class GenreService(BaseService):
    model_class: ClassVar[Type[BaseModel]] = Genre
    elastic_index: ClassVar[str] = "genres"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)
