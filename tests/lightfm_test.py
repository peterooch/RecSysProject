import pandas as pd
import numpy as np

from lightfm import LightFM
from lightfm.data import Dataset
from functools import reduce

moviedf = pd.read_parquet('parquet/movie.csv.parquet')
all_movie_genre = reduce(lambda a, b: a.union(b.split('|')), moviedf['genres'], set())

data = pd.read_csv("rate4.csv").drop(['Unnamed: 0'], axis=1)
data = data[:10000]
dataset = Dataset()
dataset.fit(data['userId'], 
            data['movieId'], 
            item_features=all_movie_genre)

movie_ids = data['movieId'].unique()
filtered = moviedf[moviedf['movieId'].apply(lambda movieid: movieid in movie_ids)]
movie_features = dataset.build_item_features(zip(filtered['movieId'], filtered['genres'].apply(lambda s: s.split('|'))))

interactions, weights = dataset.build_interactions(data.iloc[:, 0:3].values)
model = LightFM(learning_rate=0.25, loss='warp')

model.fit(interactions=interactions, item_features=movie_features)
