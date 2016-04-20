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

            #Print out results
            print('One station for specific time',specific_station_specific_time_bikes)
            print('All stations for specific time', stations_specific_time_bikes)
            print('One station for specific time', specific_station_specific_time_stands)
            print('All stations for specific time', stations_specific_time_stands)
            print(stations_specific_time_stands[0][0])
    except:
        print('Error in query')
    conn.commit()
    cur.close()
    conn.close()

def calculate_weekly(user_weekday, user_station):
    """
        Function to make call to historical data and get weekly averages for stations
    """
    conn = lite.connect('C:/Users/Connor Fitzmaurice/Documents/COMP30670/dublinbikes_database.db')
    #try:
    with conn:
        cur = conn.cursor()
        # Select available bikes

        # # Version 1, average weekly bikes just for a specific station on 1 day
        # cur.execute("SELECT AVG(Available_bikes) FROM Dynamic_Data WHERE Weekday = (?) AND Station_number = (?)",(user_weekday, user_station))
        # specific_day_specific_station_weekly_average_bikes = cur.fetchone()
        # print('\nAverage weekly bikes for One specific station on one day', specific_day_specific_station_weekly_average_bikes )
        #
        # # Version 2, average weekly bikes for specific day grouped for all stations
        # cur.execute("SELECT AVG(Available_bikes) FROM Dynamic_Data WHERE Weekday = (?) GROUP BY Station_number", (user_weekday, ))
        # specific_day_stations_weekly_average_bikes = cur.fetchall()
        # print('\nAverage weekly bikes for all stations on one day',)
        # print(specific_day_stations_weekly_average_bikes)
        # print(len(specific_day_stations_weekly_average_bikes))

        #Version 3, average weekly bikes for each each day for all stations
        cur.execute("SELECT AVG(Available_bikes) FROM Dynamic_Data GROUP BY Station_number, Weekday")
        stations_weekly_average_bikes = cur.fetchall()
        print('\nAverage weekly bikes for weekdays for all stations ', )
        print(stations_weekly_average_bikes)
        print(len(stations_weekly_average_bikes))

        # Bikes stands

        # # Version 1, average weekly stands just for a specific station on 1 day
        # cur.execute("SELECT AVG(Available_bike_stands) FROM Dynamic_Data WHERE Weekday = (?) AND Station_number = (?)",(user_weekday, user_station))
        # specific_day_specific_station_weekly_average_stands = cur.fetchone()
        # print('\nAverage weekly stands for One specific station on one day',specific_day_specific_station_weekly_average_stands)
        #
        # # Version 2, average weekly bikes for specific day grouped for all stations
        # cur.execute("SELECT AVG(Available_bike_stands) FROM Dynamic_Data WHERE Weekday = (?) GROUP BY Station_number",(user_weekday,))
        # specific_day_stations_weekly_average_stands = cur.fetchall()
        # print('\nAverage weekly stands for all stations on one day', )
        # print(specific_day_stations_weekly_average_stands)
        # print(len(specific_day_stations_weekly_average_stands))

        # Version 3, average weekly bikes for each each day for all stations
        cur.execute("SELECT AVG(Available_bike_stands) FROM Dynamic_Data GROUP BY Station_number, Weekday")
        stations_weekly_average_stands = cur.fetchall()
        print('\nAverage weekly stands for weekdays for all stations ', )
        print(stations_weekly_average_stands)
        print(len(stations_weekly_average_stands))
#Comment

    #except:
     #   print('Error in query')
    conn.commit()
    cur.close()
    conn.close()

# Test sql lite queries

def test_sql_queries():
    #calculate_daily
    past_historical_call(201603191007, 'Sat', 102)

#print("Test Starting Specific past historical call\n")
#start_time = time.clock()
#past_historical_call(user_timestamp, user_weekday, user_station)
#test_sql_queries()
#print("Completion time", time.clock() - start_time)

print("\nWeekly averages")
start_time = time.clock()
calculate_weekly('Sat', 1)
print("Completion time", time.clock() - start_time)
print("Test Ending\n\n")