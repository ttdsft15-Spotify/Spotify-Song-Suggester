from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


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
        print(request.form['songs'])
        recommendations = [
            "ABSD",
            "ASDGF",
            "ThFGHSDFGADFG",
            "rftyhertgadfg"
        ]
        return render_template("index.html", recommendations=recommendations)

    return app