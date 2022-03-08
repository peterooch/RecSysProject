import os
from random import sample
from typing import Any, Tuple, List

from joblib import load
from lightfm import LightFM
from lightfm.data import Dataset
import numpy as np

from create_model import MODEL_PATH, create_model
from lightfm_utils import similar_items

if not os.path.exists(MODEL_PATH):
    create_model()

print('Loading RecSys model from disk')
model_data: Tuple[LightFM, Dataset, Any, Any] = load(MODEL_PATH)

model, dataset, interactions, movie_features = model_data

# Create mappings for
# movielens id <=> model id
# for both users and movies
ml_to_int_uid, _, ml_to_int_mid, _ = dataset.mapping()
int_to_ml_uid = {v: k for k, v in ml_to_int_uid.items()}
int_to_ml_mid = {v: k for k, v in ml_to_int_mid.items()}

dataset_movie_ids = ml_to_int_mid.keys()
dataset_user_ids  = ml_to_int_uid.keys()

# Get 2*n top results then return n randomly selected results

def get_recommendations_by_userid(userid: int, n: int) -> List[int]:
    uid = ml_to_int_uid[userid]
    scores = model.predict(uid, np.arange(len(dataset_movie_ids)))
    sorted_mids = [mid for mid in np.argsort(-scores)]
    filtered = [int_to_ml_mid[mid] for mid in sorted_mids if not interactions[uid, mid] != 0]
    picks = sample(filtered[:2 * n], k=n)
    return picks

def get_recommendations_by_movieid(movieid: int, n: int) -> List[int]:
    mid = ml_to_int_mid[movieid]
    sim = similar_items(item_id=mid,
                        item_features=movie_features,
                        model=model,
                        N=(2 * n))
    picks = sample(list(sim['itemID']), k=n)
    return [int_to_ml_mid[mid] for mid in picks]
