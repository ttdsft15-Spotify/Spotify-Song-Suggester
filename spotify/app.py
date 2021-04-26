from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
# TODO import the model

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB = SQLAlchemy(app)

    @app.route("/", methods=['POST', 'GET'])
    def root(): 
        """Base View"""
        return render_template("index.html")


    @app.route("/suggest", methods=['POST', 'GET'])
    def suggest():
        recommendations = []
        song_selected= request.form['songs']        
        recommendations = make_recommendations(song_selected)

        return render_template("index.html", recommendations=recommendations, song=song_selected)


    """This function will call the model and make predictions"""
    def make_recommendations(song):
        
        # TODO - Use model.predict(song) 
        
        recommendations = [
            "ABSD",
            "ASDGF",
            "ThFGHSDFGADFG",
            "rftyhertgadfg"
        ]
        return recommendations

    return app