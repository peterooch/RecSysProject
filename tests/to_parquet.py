import os
import pandas as pd

for file in os.listdir("MovieLens"):
    df = pd.read_csv(f"MovieLens/{file}")
    df.to_parquet(f"parquet/{file}.parquet")
for file in os.listdir('IMDb_Kaggle'):
    df = pd.read_csv(f'IMDb_Kaggle/{file}', encoding='latin-1')
    df.to_parquet(f"parquet/{file}.parquet")