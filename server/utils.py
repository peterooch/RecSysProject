import os
import re
import string
from typing import Dict

import pandas as pd
from joblib import Memory, dump, load

from .types import Movie

ml_movies_df: pd.DataFrame = pd.read_csv('data/movie_filtered.csv', usecols=['movieId', 'title', 'genres'])
ml_link_df: pd.DataFrame = pd.read_csv('MovieLens/link.csv')

movie_reverse_index: Dict[str, int] = None

remove_year = lambda s: re.sub(r'\(\d+\)', '', s).strip()
MOVIE_RI_PATH = 'data/movie_ri.pkl'
if not os.path.exists(MOVIE_RI_PATH):
    remove_bracketed_name = lambda s: re.sub(f'\([\w\s{re.escape(string.punctuation)}]+\)', '', s).strip()
    movie_reverse_index = {
        remove_bracketed_name(remove_year(series['title'])): series['movieId'] for _, series in ml_movies_df.iterrows()
    }
    dump(movie_reverse_index, MOVIE_RI_PATH)
else:
    movie_reverse_index = load(MOVIE_RI_PATH)

memory = Memory("cache", verbose=0)
@memory.cache
def get_movie_by_id(id: int) -> Movie:
    row = ml_movies_df[ml_movies_df['movieId'] == id].T.squeeze()
    row['title'] = remove_year(row['title'])
    imdb_row = ml_link_df[ml_link_df['movieId'] == id].T.squeeze()
    row['imdb_id'] = int(imdb_row['imdbId'])
    return Movie(*row)
