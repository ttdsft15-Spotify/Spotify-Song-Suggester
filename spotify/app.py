from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd
from zipfile import ZipFile
import os.path
from os import path

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB = SQLAlchemy(app)

    @app.route("/", methods=['POST', 'GET'])
    def root(): 
        """Base View"""

        """Unzip files if they dont exist"""
        if not path.exists('tracks.csv'):
            zip = ZipFile('tracks.csv.zip')
            zip.extractall()
        else:
            print("tracks.zip exists")

        if not path.exists('NearestNeighborModel'):
            zip = ZipFile('NearestNeighborModel.zip')
            zip.extractall()
        else:
            print('NearestNeighborModel exists')

        return render_template("index.html")


    @app.route("/suggest", methods=['POST', 'GET'])
    def suggest():
        recommendations = []
        song_selected= request.form['songs']

        recommendations = make_recommendations(song_selected)

        return render_template("index.html", recommendations=recommendations, song=song_selected)


    """This function will call the model and make predictions"""
    def make_recommendations(song_name):
        recommendations = []

        # use the tracks.csv to get song details
        df = pd.read_csv('tracks.csv', parse_dates=['release_date'])
        df.dropna(inplace=True)

        song_row = df[(df.index == int(song_name))]
        print(type(song_row))
        song_row = song_row.drop(columns= ['id', 'name', 'artists', 'id_artists', 'release_date'])
        
        # Loading and running model
        NN = joblib.load('NearestNeighborModel')
        neigh_dist, neigh_index = NN.kneighbors(song_row)

        for index in neigh_index:
            recommendations.append(df['name'].iloc[index].values)
            print(df['name'].iloc[index].values)

        return recommendations

    @app.route("/reset")
    def reset():
        os.remove('tracks.csv')
        os.remove('NearestNeighborModel')
        return "Reset the models"
        
    return app