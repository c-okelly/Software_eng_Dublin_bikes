#!/usr/bin/env python
from flask import Flask, g, jsonify, render_template, current_app, request,make_response
import json
import sqlite3
# Imports for cross domain
from functools import update_wrapper
from datetime import timedelta

# Create our flask app. Static files are served from 'static' directory
app = Flask(__name__)
DATABASE = 'dublinbikes_test_database.db'
MAPS_APIKEY = 'AIzaSyBy8wTZI8iqNkK5QcB2XPusZl03xvcGV9c'
def connect_to_database():
    return sqlite3.connect(DATABASE)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Enable cross domain requests
# Code from flask website
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



# this route simply serves base html file
@app.route('/')
def root():
    return render_template('dublin_bikes.html', MAPS_APIKEY=("MAPS_APIKEY"))


@app.route("/Static_Data")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def get_stations():
    # return a list of all stations
    conn = get_db()
    cur = conn.cursor()
    stations = []
    rows = cur.execute("SELECT * from Static_Data;")
    for row in rows:
        stations.append(row)

    # Possible alternative solution. Not working as off now for more then one json object.
    # Create json object from stations list
    # json_object = []
    # for i in range(0,len(stations)):
    #     json_file = jsonify(station_no=stations[i][0],station_name=stations[i][1],address=stations[i][2],lat=stations[i][3],long=stations[i][4])
    #     json_object.append(json_file)

    # Turn list into
    json_array = json.dumps(stations)

    return json_array

##conn = get_db()
if __name__ == "__main__":
    app.run(debug=True)