import joblib
import pandas as pd


# Importing Sample Data
data_path = "./data/"
df_tracks = pd.read_csv(data_path + 'tracks.csv', parse_dates=['release_date'])
df_tracks.dropna(inplace=True)

song_row = df_tracks[df_tracks['name'] == 'Wait Until Dark']
song_row = song_row.drop(columns= ['id', 'name', 'artists', 'id_artists', 'release_date'])


# Loading and running model
NN = joblib.load('data/NearestNeighborModel')



neigh_dist, neigh_index = NN.kneighbors(song_row)
for index in neigh_index:
    print(df_tracks['name'].iloc[index])

