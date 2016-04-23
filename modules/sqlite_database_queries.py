import sqlite3 as lite # Import sql lite support
import urllib.request as request
import json
import time
import os
    
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
            cur.execute("CREATE TABLE if not exists Weekly_Averages(Station_number INT,  Weekday TEXT, Average_available_bikes INT, Average_available_bike_stands INT, PRIMARY KEY(Station_number, Weekday))")
    
            # Create hourly average table
            cur.execute("CREATE TABLE if not exists Daily_Averages(Station_number INT, Weekday TEXT, Hour INT, Average_Available_bikes INT,  Average_Available_bike_stands INT, PRIMARY KEY(Station_number, Weekday, Hour))")
    except:
        print("Error in table creation")
    conn.commit()
    cur.close()
    conn.close()
    
def populate_averages():
    conn = lite.connect('C:/Users/Connor Fitzmaurice/Documents/COMP30670/SoftwareProject/ProjectCode/dublinbikes_database.db')  
    try:
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
    except:
        print("Error in approach")
    conn.commit()
    cur.close()
    conn.close()
    
# Needs time function to run it once everyday
def update_averages():
    exit(1)
    conn = lite.connect(
        'C:/Users/Connor Fitzmaurice/Documents/COMP30670/SoftwareProject/ProjectCode/dublinbikes_database.db')
    try:
        with conn:
            cur = conn.cursor()
            #Create temporary tables
            cur.execute(
                "CREATE TABLE if not exists Weekly_Averages_temporary(Station_number INT,  Weekday_average TEXT, Average_available_bikes INT, Average_available_bike_stands INT, PRIMARY KEY(Station_number, Weekday))")
            cur.execute(
                "CREATE TABLE if not exists Daily_Averages_temporary(Station_number INT, Weekday TEXT,, Hour INT, Average_Available_bikes INT,  Average_Available_bike_stands INT, PRIMARY KEY(Station_number, Weekday, Hour))")
            #populate temporary tables
            # Populate table with Average weekly bikes and stands for each each day for all stations
            cur.execute(
                "INSERT OR IGNORE INTO Weekly_Averages_temporary(Station_number, Weekday,  Average_available_bikes,  Average_available_bike_stands)"
                "SELECT Station_number, Weekday, AVG(Available_Bikes), AVG(Available_bike_stands)"
                " FROM Dynamic_Data GROUP BY Station_number, Weekday")
    
            #  Populate table  Average hourly bikes and stands for all stations for one week
            cur.execute(
                "INSERT OR IGNORE INTO Daily_Averages_temporary(Station_number, Weekday, Hour, Average_available_bikes, Average_available_bike_stands)"
                "SELECT Station_number, Weekday, Timestamp,(Timestamp % 10000)/100, AVG(Available_bikes), AVG(Available_bike_stands) "
                "FROM Dynamic_Data GROUP BY Station_number, Weekday, (Timestamp % 10000)/100")
    
            # Update average tables using temporary
            cur.execute("UPDATE Weekly_Averages SET Station_number, Weekday,  Average_available_bikes,  Average_available_bike_stands "
                        "FROM (SELECT Station_number, Weekday,  Average_available_bikes,  Average_Available_bike_stands FROM Weekly_Averages_temporary)"
                        "WHERE Weekly_Averages.Station_number = Weekly_Averages_temporary.Station_number"
                        "and Weekly_Averages.Weekday = Weekly_Averages_temporary.Weekday")
            cur.execute(
                "UPDATE Daily_Averages SET Station_number, Weekday, Hour, Average_available_bikes, Average_available_bike_stands)"
                "FROM (SELECT Station_number, Weekday,  Hour, Average_available_bikes,  Average_available_bike_stands FROM Daily_Averages_temporary)"
                "WHERE Daily_Averages.Station_number = Daily_Averages_temporary.Station_number"
                "and Daily_Averages.Weekday = Daily_Averages_temporary.Weekday and Daily_Averages.Hour = Daily_Averages_temporary.Hour")
    
            # Drop temporary tables
            cur.execute("DROP Daily_Averages_temporary")
            cur.execute("DROP Weekly_Averages_temporary")
    except:
        print('Error in updating average tables')
    conn.commit()
    cur.close()
    conn.close()
