#!/usr/bin/env python
from flask import Flask, g, jsonify, render_template
import json
import sqlite3
# Create our flask app. Static files are served from 'static' directory
app = Flask(__name__)
DATABASE = 'dublinbikes_test_database.db'
MAPS_APIKEY = 'AIzaSyBy8wTZI8iqNkK5QcB2XPusZl03xvcGV9c'
def connect_to_database():
    return sqlite3.connect([DATABASE])


def get_db():
    db = getattr(g, DATABASE, None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, DATABASE, None)
    if db is not None:
        db.close()




# this route simply serves base html file
@app.route('/')
def root():
    return render_template('dublin_bikes.html', MAPS_APIKEY=("MAPS_APIKEY"))


@app.route("/Static_Data")
def get_stations():
    # return a list of all stations
    conn = get_db()
    cur = conn.cursor()
    stations = []
    rows = cur.execute("SELECT * from Static_Data;")
    for row in rows:
        stations.append(row)

    return jsonify(stations=stations)

##conn = get_db()
if __name__ == "__main__":
    app.run(debug=True)