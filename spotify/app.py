from flask import Flask, redirect, render_template, request
import joblib
import pandas as pd
import os.path
from os import path
from flask_sqlalchemy import SQLAlchemy
import sqlite3

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB = SQLAlchemy(app)

    # Read the CSV file into a df
    df = pd.read_csv('./data/df_with_topics.csv', parse_dates=['release_date'])
    df.drop(columns=['Unnamed: 0'], inplace=True)

    # create a SQLITE connection
    conn = sqlite3.connect("db.sqlite3")

    # check to see if the table already exists
    count = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='merged';").fetchall()

    if not count:
        print("GOING TO CREATE A TABLE CALLED MERGED")
        # upload the df to a table
        df.to_sql("merged", conn)

    # close the SQL connection
    conn.close

    @app.route("/", methods=['POST', 'GET'])
    def root(): 
        """Base View"""
        return render_template("index.html")


    @app.route("/search", methods=['POST', 'GET'])
    def search(): 
        """Search View"""

        song = request.form.get('song', False)
        song = "%" + str(song) + "%"

        # create a SQLITE connection
        conn = sqlite3.connect('db.sqlite3')
        curs = conn.cursor()
        results = curs.execute("SELECT [index], name, Artist FROM merged WHERE name like (?) ", (song,)).fetchall()
        return render_template("search.html", results=results)

    @app.route("/search_suggest", methods=['POST', 'GET'])
    def search_suggest():
        recommendations = []
        selected_song_index= request.form.get('selection_id', False)

        song_name, artist, recommendations, artists = make_recommendations(selected_song_index)

        return render_template("search.html", recommendations=recommendations, song=song_name, artists=artists, artist=artist)


    @app.route("/suggest", methods=['POST', 'GET'])
    def suggest():
        recommendations = []
        selected_song_index= request.form['songs']

        song_name, artist, recommendations, artists = make_recommendations(selected_song_index)

        return render_template("index.html", recommendations=recommendations, song=song_name, artists=artists, artist=artist)


    """This function will call the model and make predictions"""
    def make_recommendations(selected_song_index):
        recommendations = []
        artists = []

        #  load the tracks.csv into a Pandas dataframe
        df = pd.read_csv('./data/df_with_topics.csv', parse_dates=['release_date'])
        # drop nulls
        df.dropna(inplace=True)

        # use the tracks.csv to get song details based on the song index
        song_row = df[(df.index == int(selected_song_index))]

        # get the name of the song as it is displayed in the dataframe
        song_name = song_row['name'].values[0]
        artist = song_row['Artist'].values[0]

        # drop columns in preparation for model call
        # song_row = song_row.drop(columns= ['id', 'name', 'Artist', 'id_artists', 'release_date'])

        # Pass the dataframe to the wrangle function given by unit4
        song_row = keep_wanted_columns(song_row)
        
        # Loading and running model
        NN = joblib.load('./data/NearestNeighborModelWithTopics')
        neigh_dist, neigh_index = NN.kneighbors(song_row)

        # get the list of song recommendations from the model
        for index in neigh_index[0]:
            recommendations.append(df['name'].iloc[index].title())
            artists.append(df['Artist'].iloc[index].title())


        recommendations = recommendations[1:]
        artists = artists[1:]

        # return selected song name and recommendations 
        return song_name, artist, recommendations, artists


    def keep_wanted_columns(df):
        df_dropped = df[['popularity', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'new_topic_name_Existential', 'new_topic_name_Religion',
            'new_topic_name_Gangsta', 'new_topic_name_Poppy','new_topic_name_Love']]

        return df_dropped

    return app