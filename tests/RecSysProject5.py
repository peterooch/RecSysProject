#!/usr/bin/env python
# coding: utf-8

# In[1]:

from re import M
import pandas as pd
import numpy as np
from datetime import datetime 

start_time = datetime.now() 

df = pd.read_csv("rate4.csv")
df = df.drop(['Unnamed: 0'], axis=1)

# In[2]:

df = df[:100000]
#df = df

df

# In[3]:

df.info()

# In[4]:

import sys
import os

import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import lightfm
from lightfm import LightFM
from lightfm.data import Dataset
from lightfm import cross_validation

# Import LightFM's evaluation metrics
from lightfm.evaluation import precision_at_k as lightfm_prec_at_k
from lightfm.evaluation import recall_at_k as lightfm_recall_at_k

# Import repo's evaluation metrics
#from recommenders.evaluation.python_evaluation import (precision_at_k, recall_at_k)

#from recommenders.utils.timer import Timer
#from recommenders.datasets import movielens
#from recommenders.models.lightfm.lightfm_utils import (
#    track_model_metrics, prepare_test_df, prepare_all_predictions,
#    compare_metric, similar_users, similar_items)


#Import repo's evaluation metrics
#from recommenders.evaluation.python_evaluation import (precision_at_k, recall_at_k)

from recommenders.utils.timer import Timer
#from recommenders.datasets import movielens
from lightfm_utils import (
   track_model_metrics, prepare_test_df, prepare_all_predictions,
   compare_metric, similar_users, similar_items)


print("System version: {}".format(sys.version))
print("LightFM version: {}".format(lightfm.__version__))

# In[5]:

# Select MovieLens data size
MOVIELENS_DATA_SIZE = str(len(df))

# default number of recommendations
K = 10
# percentage of data used for testing
TEST_PERCENTAGE = 0.25
# model learning rate
LEARNING_RATE = 0.25
# no of latent factors
NO_COMPONENTS = 20
# no of epochs to fit model
NO_EPOCHS = 20
# no of threads to fit model
NO_THREADS = 32
# regularisation for both user and item features
ITEM_ALPHA=1e-6
USER_ALPHA=1e-6

# seed for pseudonumber generations
SEEDNO = 42
# In[6]:

# data = movielens.load_pandas_df(
#     size=MOVIELENS_DATA_SIZE,
#     genres_col='genre',
#     header=["userID", "itemID", "rating"]
# )

data = df
# quick look at the data
data.sample(5)
# In[7]:
dataset = Dataset()
# In[8]:

dataset.fit(users=data['userId'], 
            items=data['movieId'])

# quick check to determine the number of unique users and items in the data
num_users, num_topics = dataset.interactions_shape()
print(f'Num users: {num_users}, num_topics: {num_topics}.')

# In[9]:

(interactions, weights) = dataset.build_interactions(data.iloc[:, 0:3].values)

# In[10]:

train_interactions, test_interactions = cross_validation.random_train_test_split(
    interactions, test_percentage=TEST_PERCENTAGE,
    random_state=np.random.RandomState(SEEDNO))

# In[11]:

print(f"Shape of train interactions: {train_interactions.shape}")
print(f"Shape of test interactions: {test_interactions.shape}")

# In[12]:

model1 = LightFM(loss='warp', no_components=NO_COMPONENTS, 
                 learning_rate=LEARNING_RATE,                 
                 random_state=np.random.RandomState(SEEDNO))

# In[13]:

model1.fit(interactions=train_interactions,
          epochs=NO_EPOCHS)

# In[14]:
uids, iids, interaction_data = cross_validation._shuffle(
    interactions.row, interactions.col, interactions.data, 
    random_state=np.random.RandomState(SEEDNO))

cutoff = int((1.0 - TEST_PERCENTAGE) * len(uids))
test_idx = slice(cutoff, None)

# In[15]:
uid_map, ufeature_map, iid_map, ifeature_map = dataset.mapping()
# In[ ]:
# In[16]:
# df2 = pd.read_csv("Desktop\Recommender Systems Project\MovieLens_Kaggle\\archive\movie.csv")
# df2

# user_feature_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k/u.user'
# user_data = pd.read_table(user_feature_URL, 
#               sep='|', header=None)
# user_data.columns = ['userID','age','gender','occupation','zipcode']

# # merging user feature with existing data
# new_data = data.merge(user_data[['movieId','genres']], left_on='movieId', right_on='movieId')
# # quick look at the merged data
# new_data.sample(5)

# In[17]:
df2 = pd.read_csv("MovieLens\movie.csv")
df2

movie_genre = [x.split('|') for x in df2['genres']]

# retrieve the all the unique genres in the data
all_movie_genre = sorted(list(set(itertools.chain.from_iterable(movie_genre))))
# quick look at the all the genres within the data
all_movie_genre
# In[ ]:
# In[18]:
dataset2 = Dataset()
dataset2.fit(data['userId'], 
            data['movieId'],
            item_features=all_movie_genre)
            #user_features=all_occupations)
# In[19]:
item_features = dataset2.build_item_features(
    (x, y) for x,y in zip(data.movieId, movie_genre))
# In[20]:
(interactions2, weights2) = dataset2.build_interactions(data.iloc[:, 0:3].values)

#print(interactions2)
#print(weights2)

train_interactions2, test_interactions2 = cross_validation.random_train_test_split(
    interactions2, test_percentage=TEST_PERCENTAGE,
    random_state=np.random.RandomState(SEEDNO))
# In[21]:
model2 = LightFM(loss='warp', no_components=NO_COMPONENTS, 
                 learning_rate=LEARNING_RATE, 
                 item_alpha=ITEM_ALPHA,
                 user_alpha=USER_ALPHA,
                 random_state=np.random.RandomState(SEEDNO))
# In[22]:
model2.fit(interactions=interactions2,
           #user_features=user_features,
           item_features=item_features,
           epochs=NO_EPOCHS)
# In[23]:
# _, user_embeddings = model2.get_user_representations(features=user_features)
# user_embeddings
# In[24]:
# similar_users(user_id=1, user_features=user_features, 
#             model=model2)
# In[25]:
_, item_embeddings = model2.get_item_representations(features=item_features)
item_embeddings

#print(item_embeddings)
def movieid_to_row_id(movieid: int) -> int:
    return movieid

item_id = movieid_to_row_id(1)

# In[26]:
sim = similar_items(item_id=item_id, item_features=item_features, 
            model=model2)
sim
# In[27]:
df2
# In[28]:
print('The movie:')
for i in range(len(df2)):
    if df2['movieId'][i] == item_id:
        print((df2['movieId'][i], df2['title'][i], df2['genres'][i]))

print()
print()
print('Recommended movies:')

for i in range(len(sim)):
    for j in range(len(df2)):
        if df2['movieId'][j] == sim['itemID'][i]:
            print((df2['movieId'][j], df2['title'][j], df2['genres'][i]))

# In[ ]:

# In[29]:
print('Time elapsed in (hh:mm:ss.ms): "{}"'.format(datetime.now() - start_time))