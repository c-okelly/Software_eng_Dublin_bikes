import sqlite3 as lite # Import sql lite support
import urllib.request as request
import json
import time
import os

def past_historical_call(user_timestamp, user_weekday, user_station):
    """
        Function to make call to historical data and get information for stations at a specific time
    """
    conn = lite.connect('C:/Users/Connor Fitzmaurice/Documents/COMP30670/dublinbikes_database.db')
    try:
        with conn:
            cur = conn.cursor()
            # Select available bikes

            # Version 1, just for a specific station
            cur.execute("SELECT Available_bikes FROM Dynamic_Data WHERE Timestamp = (?) AND Weekday = (?) AND Station_number = (?)", (user_timestamp, user_weekday, user_station))
            specific_station_specific_time_bikes = cur.fetchone()
            # Version 2, just for all stations
            cur.execute("SELECT Available_bikes FROM Dynamic_Data WHERE Timestamp = (?) AND Weekday = (?)", (user_timestamp, user_weekday))
            stations_specific_time_bikes = cur.fetchall()

            # Select available stands
            # Version 1, just for a specific station
            cur.execute("SELECT Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (?) AND Weekday = (?) AND Station_number = (?)",(user_timestamp, user_weekday, user_station))
            specific_station_specific_time_stands = cur.fetchone()
            # Version 2, just for all stations
            cur.execute("SELECT Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (?) AND Weekday = (?)",(user_timestamp, user_weekday))
            stations_specific_time_stands = cur.fetchall()
    except:
        print('Error in query')
    conn.commit()
    cur.close()
    conn.close()
