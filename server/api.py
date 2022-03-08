from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import (
    dataset_user_ids, get_recommendations_by_userid,
    get_recommendations_by_movieid
)
from .types import Movie, UserList, RecommenderMethod
from .utils import get_movie_by_id, movie_reverse_index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users", response_model=UserList)
async def get_users():
    '''
    Returns a list of all users ids in the recommender system
    '''
    return UserList(sorted(dataset_user_ids))

sorted_movie_names = sorted(movie_reverse_index.keys())
@app.get("/movies", response_model=List[str])
async def get_movies():
    '''
    Returns a list of all the relevant movies in the recommender system
    '''
    return list(sorted_movie_names)

@app.get("/recommendations/", response_model=List[Movie])
async def get_recommendations(method: RecommenderMethod, param: str, n_recommends: Optional[int] = 10):
    '''
    Get `n_recommends` amount of recommended movies depending on the received `method` and `param` parameters.

    `method` parameter can be either `movie` for content-based filtering or
    `userid` for collabarative filtering.

    `param` parameter depends on the selected `method`, with `userid` requiring an `int` 0 or bigger,
    and `movie` requires a movie title.
    '''

    userid = 0
    # sanity check
    if method == RecommenderMethod.UserID and param != "":
        try:
            userid = int(param)
            if userid not in dataset_user_ids:
                raise ValueError(f'User ID {userid} not found in dataset')
        except ValueError:
            return []
    if method == RecommenderMethod.UserID:
        return [get_movie_by_id(mid) for mid in get_recommendations_by_userid(userid, n_recommends)]

    # method is Movie
    if param not in movie_reverse_index:
        return []
    movieid = movie_reverse_index[param]
    return [get_movie_by_id(mid) for mid in get_recommendations_by_movieid(movieid, n_recommends)]    
