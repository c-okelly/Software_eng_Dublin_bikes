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
            # Select available bike ands stands

            # Version 1,  just for a specific station
            cur.execute("SELECT Available_bikes, Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (?) AND Weekday = (?) AND Station_number = (?)", (user_timestamp, user_weekday, user_station))
            specific_station_specific_time_bikes = cur.fetchone()
            # Version 2, just for all stations
            cur.execute("SELECT Station_number, Available_bikes,  Available_bike_stands FROM Dynamic_Data WHERE Timestamp = (?) AND Weekday = (?)", (user_timestamp, user_weekday))
            stations_specific_time_bikes = cur.fetchall()

    except:
        print('Error in query')
    conn.commit()
    cur.close()
    conn.close()
    
def create_average_tables():
    """
        Fuction to create averages tables for database to allow for faster queries.
        :return: None
    """
    conn = lite.connect('C:/Users/Connor Fitzmaurice/Documents/COMP30670/SoftwareProject/ProjectCode/dublinbikes_database.db')
    try:
        with conn:
            cur = conn.cursor()
    
            # Create weekly average table
            cur.execute("CREATE TABLE if not exists Weekly_Averages(Station_number INT,  Weekday_average TEXT, Average_available_bikes INT, Average_available_bike_stands INT, PRIMARY KEY(Station_number, Weekday))")
    
            # Create hourly average table
            cur.execute("CREATE TABLE if not exists Daily_Averages(Station_number INT, Weekday TEXT, Hour INT, Average_Available_bikes INT,  Average_Available_bike_stands INT, PRIMARY KEY(Station_number, Weekday, Hour))")
    except:
        print("Error in table creation")
    conn.commit()
    cur.close()
    conn.close()
    
def populate_averages():
    conn = lite.connect('C:/Users/Connor Fitzmaurice/Documents/COMP30670/SoftwareProject/ProjectCode/dublinbikes_database.db')
    #try:
    with conn:
        cur = conn.cursor()
        # Populate table with Average weekly bikes and stands for each each day for all stations
        cur.execute("INSERT OR IGNORE INTO Weekly_Averages(Station_number, Weekday,  Average_available_bikes,  Average_Available_bike_stands)"
                    "SELECT Station_number, Weekday, AVG(Available_Bikes), AVG(Available_bike_stands)"
                    " FROM Dynamic_Data GROUP BY Station_number, Weekday")

        #  Populate table  Average hourly bikes and stands for all stations for one week
        cur.execute( "INSERT OR IGNORE INTO Daily_Averages(Station_number, Weekday, Hour, Average_available_bikes, Average_Available_bike_stands)"
                     "SELECT Station_number, Weekday, (Timestamp % 10000)/100, AVG(Available_bikes), AVG(Available_bike_stands) "
                     "FROM Dynamic_Data GROUP BY Station_number, Weekday, (Timestamp % 10000)/100")
    #except:
     #print("Error in approach")
    conn.commit()
    cur.close()
    conn.close()
