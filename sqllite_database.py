__author__ = 'Connor Fitzmaurice'


import sqlite3 as lite # Import sql lite support
import urllib.request as request
import json
import time
import os

def create_database(static_data):
    """
        Fuction to create database. Calls functions to create tables and import pre-exisitng data
    """
    conn = lite.connect('C:\\Users\\Connor Fitzmaurice\\Documents\\COMP30670\\dublinbikes_test_database.db') # connect () works by searching for a database file and connecting to it
    with conn: # Run only if connection is made (optional)
        cur = conn.cursor() # Cursor class which is used to execute SQL statements

        # Create dynamic table
        cur.execute("CREATE TABLE if not exists Dynamic_Data(Station_number INT, Timestamp INT, Last_update REAL, Status TEXT, Bike_stands INT, Available_bike_stands INT, Available_bikes INT , PRIMARY KEY(Station_number, Timestamp))")

        #Create Static table with primary and foreign keys
        cur.execute("CREATE TABLE if not exists Static_Data(station_number INT PRIMARY KEY, Name TEXT, Address TEXT, Latitude REAL, Longitude REAL,  FOREIGN KEY(station_number) REFERENCES Dynamic_Data(station_number))")
        #cur.executemany("INSERT INTO Static_Data ('Latitude','Address','station_number','name','Longtitude') VALUES('?','?','?','?','?')", static_data)
        for i in range(1,103):
            if i != 50:
                station_index = static_data[i]
                print(station_index)
                cur.execute("INSERT INTO Static_Data(station_number, Name, Address, Latitude, Longitude) VALUES(?,?,?,?,?)", (station_index['number'], station_index['name'], station_index['address'], station_index['latitude'], station_index['longitude']))

    conn.commit()
    cur.close()
    conn.close()# Close connection to allow for tables to be created in seperate functions

    #import_historical_data()
    #import_dynamic_data()

def import_historical_data():
    """
        Import historical dynamic data. Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return: None
    """
    conn = lite.connect('dublinbikes_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        path = "/var/www/html/"
        dirs = os.listdir( path )

        # This would print all the files and directories
    for file in dirs:
        for i in range(1,103):
            if i != 50:
                station_index = static_data[i]
        cur.executemany("INSERT INTO Dynamic_Data (Station_number, Timestamp, Last_update, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES('?','?','?','?','?','?','?')", historical_data_superdictionary_stations)
    conn.commit()
    cur.close()
    conn.close()

def import_dynamic_data():
    """
        Import dynamic . Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return:
    """
    #Connect to database
    conn = lite.connect('dublinbike_test_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        cur.executemany("INSERT INTO Dynamic_Data (station_number, Timestamp, Last_update, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES('?','?','?','?','?','?','?')", superdicitonary_stations)
    conn.commit() #Redundant here
    cur.close()
    conn.close()

def database_backup(database, backup):
    """
        Function to backup database
        :return:
    """
    #Backup to sql file
    conn = lite.connect('dublinbike_test_database.db',  isolation_level = None)
    with open('test4_backup.sql', 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)

def data_retrieval():
    """
        Fucntion to query database
        :return:
    """
    # Connect to database
    conn = lite.connect('dublinbike_test_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM Dynamic_Data')

        rows = cur.fetchall()

        for row in rows:
            print(row)
    cur.close()
    conn.close()

def return_static_data(city="Dublin",directory_to_save_to="Data/"):
    # Defualt city is set to Dublin.

    # Call static data and save
    # Set url for static data call. Json format
    url = "https://developer.jcdecaux.com/rest/vls/stations/" + city + ".json"

    #Request and get json file
    static_json_file = request.urlopen(url).read()

    # Convert file to UTF-8
    static_json_file = static_json_file.decode("UTF-8")

    # Convert each station to a list of dicts
    static_json_dicts = json.loads(static_json_file)

    # Station dict
    static_station_dict = {}

    # Format so each station can be called by station number.
    for item in static_json_dicts:
        key = item.get("number")
        sub_dict = item
        static_station_dict.update({key:sub_dict})

    # Check data directory exists
    if not os.path.exists(directory_to_save_to):
        os.makedirs(directory_to_save_to)

    # Save static data to file
    file_name = directory_to_save_to + "Static_data_for_" + city
    with open(file_name, 'a') as f:
        json.dump(static_station_dict, f, ensure_ascii=False)

    return static_station_dict


static_data_dict = return_static_data()
#print(static_data_dict)
create_database(static_data_dict)