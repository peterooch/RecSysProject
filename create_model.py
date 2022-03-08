
from os import makedirs, path
from itertools import count, chain

from lightfm import LightFM
from lightfm.data import Dataset
import pandas as pd
from joblib import dump, load

MODEL_PATH = "data/model_data.pkl"
FEATURE_PATH = "data/movie_features.pkl"
# Create model for use
# Preprocess, train, fit....#
#
def get_features(moviedf):
    ml_link_df: pd.DataFrame = pd.read_csv('MovieLens/link.csv')
    imdb_df: pd.DataFrame = pd.read_csv('IMDb_Kaggle/IMDb movies.csv', encoding='latin-1')
    counter = count(1, 1)
    for movieid, genres in zip(moviedf['movieId'], moviedf['genres']):
        print(f'Extracting features from movie {next(counter)} out of {len(moviedf)}', end='\r')
        features = genres.split('|')
        imdb_row = ml_link_df[ml_link_df['movieId'] == movieid].T.squeeze()
        imdb_id = str(int(imdb_row['imdbId']))
        imdb_row = imdb_df[imdb_df['imdb_title_id'].apply(lambda s: imdb_id in s)]
        if len(imdb_row) == 1:
            imdb_row = imdb_row.T.squeeze()
            features += imdb_row['director'].split(',')
            features += imdb_row['actors'].split(',')

        yield [feature.lower().strip() for feature in features]
    print('\nMovie feature extraction done')

def create_model():
    makedirs('data', exist_ok=True)
    print('Building RecSys model')

    # csv file with (userid, movieid, rating) tuples
    data = pd.read_csv("rate4.csv", usecols=['userId', 'movieId', 'rating'])

    movie_ids = data['movieId'].unique()
    moviedf = pd.read_csv('MovieLens/movie.csv')

    filtered = moviedf[moviedf['movieId'].apply(lambda movieid: movieid in movie_ids)]
    filtered.to_csv('data/movie_filtered.csv')
    if not path.exists(FEATURE_PATH):
        features = list(get_features(filtered))
        dump(features, FEATURE_PATH)
        print('Saved movie features to disk')
    else:
        features = load(FEATURE_PATH)
        print('Loaded movie features from disk')


    dataset = Dataset()
    dataset.fit(data['userId'].append(pd.Series([0])), # add id 0, which is a user without any ratings 
                data['movieId'], 
                item_features=chain.from_iterable(features))

    movie_features = dataset.build_item_features(zip(filtered['movieId'], features))

    interactions, weights = dataset.build_interactions(data.iloc[:, 0:3].values)
    '''
    for i in range(len(weights.data)):
        if weights.data[i] < 3:
            interactions.data[i] = -1
        else:
            interactions.data[i] = 1
    '''     

    model = LightFM(loss='warp', random_state=42)

    model.fit(interactions=interactions,
              item_features=movie_features,
              epochs=30,
              num_threads=4,
              verbose=True)

    print('Saving RecSys model to disk')
    dump((model, dataset, interactions.tocsr(), movie_features), MODEL_PATH, compress=True) 

# Debugging 'feature' if only model creation is needed to be checked
if __name__ == "__main__":
    create_model()
