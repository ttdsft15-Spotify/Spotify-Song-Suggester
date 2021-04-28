from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd
from zipfile import ZipFile
import os.path
from os import path

def create_app():

    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # DB = SQLAlchemy(app)

    @app.route("/", methods=['POST', 'GET'])
    def root(): 
        """Base View"""
        return render_template("index.html")


    @app.route("/suggest", methods=['POST', 'GET'])
    def suggest():
        recommendations = []
        selected_song_index= request.form['songs']

        song_name, recommendations = make_recommendations(selected_song_index)

        return render_template("index.html", recommendations=recommendations, song=song_name)


    """This function will call the model and make predictions"""
    def make_recommendations(selected_song_index):
        recommendations = []

        #  load the tracks.csv into a Pandas dataframe
        df = pd.read_csv('./data/df_with_topics.csv', parse_dates=['release_date'])
        # drop nulls
        df.dropna(inplace=True)

        # use the tracks.csv to get song details based on the song index
        song_row = df[(df.index == int(selected_song_index))]

        # get the name of the song as it is displayed in the dataframe
        song_name = song_row['name'].values[0]

        # drop columns in preparation for model call
        # song_row = song_row.drop(columns= ['id', 'name', 'Artist', 'id_artists', 'release_date'])

        # Pass the dataframe to the wrangle function given by unit4
        song_row = keep_wanted_columns(song_row)
        
        # Loading and running model
        NN = joblib.load('./data/NearestNeighborModelWithTopics')
        neigh_dist, neigh_index = NN.kneighbors(song_row)

        # get the list of song recommendations from the model
        for index in neigh_index:
            recommendations = df['name'].iloc[index].values.tolist()

        recommendations = recommendations[1:]

        # return selected song name and recommendations 
        return song_name, recommendations


    def keep_wanted_columns(df):
        df_dropped = df[['popularity', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'new_topic_name_Existential', 'new_topic_name_Religion',
            'new_topic_name_Gangsta', 'new_topic_name_Poppy','new_topic_name_Love']]

        return df_dropped

    return app