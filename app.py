#!/usr/bin/env python
from flask import Flask, g, jsonify, render_template, current_app, request,make_response
import json
import sqlite3
# Imports for cross domain
from functools import update_wrapper
from datetime import timedelta

# Create our flask app. Static files are served from 'static' directory
app = Flask(__name__)
DATABASE = 'Database/dublinbikes_database.db'
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
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def root():
    return "hello"#render_template('website/dublin_bikes.html', MAPS_APIKEY=("MAPS_APIKEY"))


@app.route("/Latest_Data")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def get_stations():
    # return a list of all stations
    conn = get_db()
    cur = conn.cursor()

    static_stations = []
    rows = cur.execute("SELECT * from Static_Data;")
    for row in rows:
        static_stations.append(row)
        
    # Turn list into
    no_stations = len(static_stations)
    stations_dict = {}
    for i in range(0, len(static_stations)):
        stations_dict[i] = {"Station_no":static_stations[i][0],"Station_name":static_stations[i][1],"Station_address":static_stations[i][2],"Lat":static_stations[i][3],"Long":static_stations[i][4]}
    # Add no stations varailbe to dict
    stations_dict["no_stations"] = no_stations


    # Live info
    live_stations = []
    live_rows = cur.execute("SELECT Timestamp, Station_number, Bike_stands, Available_bikes, Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (SELECT Timestamp FROM Dynamic_Data ORDER BY TimeStamp DESC LIMIT 1);")
    for i in live_rows:
        live_stations.append(i)

    # Turn list into
    live_data = {}
    for i in range(0, len(live_stations)):
        live_data[i] = {"Timestamp":live_stations[i][0], "Station_no":live_stations[i][1], "No_bike_stands":live_stations[i][2],"Available_bikes":live_stations[i][3],"Available_bike_stands":live_stations[i][4]}

    total_ob = {"Static_data":stations_dict, "Station_info":live_data}
    json_array = json.dumps(total_ob)

    return json_array

# Test of inputing varialbes
@app.route("/Historical_Call/<Timestamp>")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def Hist_call(Timestamp):
        conn = get_db()
        cur = conn.cursor()
        histarray = []
        hrows = cur.execute(("SELECT Station_number, Bike_stands, Available_bikes, Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (?) GROUP BY Station_number"),(Timestamp,))
        for row in hrows:
            histarray.append(row)

        # Turn list into
        Hist_dict = {}
        for i in range(0, len(histarray)):
            Hist_dict[i] = {"Station_no":histarray[i][0], "No_bike_stands":histarray[i][1],"Available_bikes":histarray[i][2],"Available_bike_stands":histarray[i][3]}

        static_stations = []
        rows = cur.execute("SELECT * from Static_Data;")
        for row in rows:
            static_stations.append(row)

        # Turn list into
        no_stations = len(static_stations)
        stations_dict = {}
        for i in range(0, len(static_stations)):
            stations_dict[i] = {"Station_no":static_stations[i][0],"Station_name":static_stations[i][1],"Station_address":static_stations[i][2],"Lat":static_stations[i][3],"Long":static_stations[i][4]}
        # Add no stations varailbe to dict
        stations_dict["no_stations"] = no_stations

        total_ob = {"Static_data": stations_dict, "Station_info": Hist_dict}
        json_array = json.dumps(total_ob)

        return json_array

@app.route("/Hourly_call/<day_of_week>/<hour>")
@crossdomain(origin='*') # Allow crossdomain request for this funciton any origin
def Hist_hourly_call(day_of_week,hour):
        conn = get_db()
        cur = conn.cursor()
        Hourarray = []
        hourrows = cur.execute(("SELECT Station_number, Average_Available_bikes, Average_Available_bike_stands, Weekday, Hour FROM Daily_Averages where Weekday = (?) and Hour = (?)"),(day_of_week,hour))
        for row in hourrows:
            Hourarray.append(row)
        # print(row)

        # Turn list into
        hourly_average_dict = {}
        for i in range(0, len(Hourarray)):
            total_stands = Hourarray[i][1] + Hourarray[i][2]
            hourly_average_dict[i] = {"Station_no":Hourarray[i][0], "No_bike_stands":total_stands,"Available_bikes":Hourarray[i][1],"Available_bike_stands":Hourarray[i][2],"Day_the_week":Hourarray[i][3], "Hour":Hourarray[i][4]}

        static_stations = []
        rows = cur.execute("SELECT * from Static_Data;")
        for row in rows:
            static_stations.append(row)

        ## Turn list into
        no_stations = len(static_stations)
        stations_dict = {}
        for i in range(0, len(static_stations)):
            stations_dict[i] = {"Station_no":static_stations[i][0],"Station_name":static_stations[i][1],"Station_address":static_stations[i][2],"Lat":static_stations[i][3],"Long":static_stations[i][4]}
        # Add no stations varailbe to dict
        stations_dict["no_stations"] = no_stations

        total_ob = {"Static_data": stations_dict, "Station_info": hourly_average_dict}
        json_array = json.dumps(total_ob)

        return json_array


if __name__ == "__main__":
    app.run()
    #app.run(debug=True)