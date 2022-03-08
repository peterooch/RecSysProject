
from enum import Enum
from typing import List

from pydantic.dataclasses import dataclass

@dataclass
class UserList:
    users: List[int]

class RecommenderMethod(Enum):
    UserID = "userid"
    Movie = "movie"

@dataclass
class Movie:
    id: int
    title: str
    genres: str
    imdb_id: str
