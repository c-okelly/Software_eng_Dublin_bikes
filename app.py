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


@app.route("/Latest_Data")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def get_stations():
    # return a list of all stations
    conn = get_db()
    cur = conn.cursor()
    stations = []
    rows = cur.execute("SELECT * from Static_Data;")
    for row in rows:
        stations.append(row)
        
    # Turn list into
    stations_dict = {}
    for i in range(0,len(stations)):
        stations_dict[i] = stations[i]

    # Live info
    live_stations = []
    live_rows = cur.execute("SELECT Station_number, Timestamp, Bike_stands, Available_bikes, Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (SELECT Timestamp FROM Dynamic_Data ORDER BY TimeStamp DESC LIMIT 1);")
    for i in live_rows:
        live_stations.append(i)
    print(live_stations)

    live_data = {}
    for i in range(0,len(live_stations)):
        live_data[i] = live_stations[i]

    total_ob = {"Static_data":stations_dict, "Live_info":live_data}
    json_array = json.dumps(total_ob)

    return json_array

# Test of inputing varialbes
@app.route("/Historical_Call/<Timestamp>")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def Hist_call(Timestamp):
        conn = get_db()
        cur = conn.cursor()
        histarray = []
        hrows = cur.execute(("SELECT Station_number, Available_bikes, Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (?) GROUP BY Station_number"),(Timestamp,))
        for row in hrows:
            histarray.append(row)

        # Turn list into
        Hist_dict = {}
        for i in range(0, len(histarray)):
            Hist_dict[i] = histarray[i]

        stations = []
        rows = cur.execute("SELECT * from Static_Data;")
        for row in rows:
            stations.append(row)

        # Turn list into
        stations_dict = {}
        for i in range(0, len(stations)):
            stations_dict[i] = stations[i]






        total_ob = {"Historical data": Hist_dict, "Static Data": stations_dict}
        json_array = json.dumps(total_ob)

        return json_array

@app.route("/Hourly_call/<day_of_week>/<hour>")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def Hist_hourly_call(day_of_week,hour):
        conn = get_db()
        cur = conn.cursor()
        Hourarray = []
        hourrows = cur.execute(("SELECT Station_number, Weekday, Hour, Average_Available_bikes, Average_Available_bike_stands FROM Daily_Averages where Weekday = (?) and Hour = (?)"),(day_of_week,hour))
        for row in hourrows:
            Hourarray.append(row)

        # Turn list into
        Hour_dict = {}
        for i in range(0, len(Hourarray)):
            Hour_dict[i] = Hourarray[i]

        stations = []
        rows = cur.execute("SELECT * from Static_Data;")
        for row in rows:
            stations.append(row)

        # Turn list into
        stations_dict = {}
        for i in range(0, len(stations)):
            stations_dict[i] = stations[i]

        total_ob = {"Hourly data": Hour_dict, "Static Data": stations_dict}
        json_array = json.dumps(total_ob)

        return json_array




##conn = get_db()
if __name__ == "__main__":
    app.run(debug=True)