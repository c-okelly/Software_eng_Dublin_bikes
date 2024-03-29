__author__ = 'Connor Fitzmaurice'


import sqlite3 as lite # Import sql lite support
import urllib.request as request
import json
import time
import os

def create_database(static_data, data_directory , data_directory_files):
    """
        Fuction to create database. Calls functions to create tables and import static and pre-exisitng data
        :return: None
    """
    conn = lite.connect('dublinbikes_test_database.db') # connect () works by searching for a database file and connecting to it
    with conn: # Run only if connection is made (optional)
        cur = conn.cursor() # Cursor class which is used to execute SQL statements

        # Create dynamic table with primary key
        cur.execute("CREATE TABLE if not exists Dynamic_Data(Station_number INT, Timestamp INT, Last_update REAL,  Weekday TEXT, Status TEXT, Bike_stands INT, Available_bike_stands INT, Available_bikes INT , PRIMARY KEY(Station_number, Timestamp))")

        #Create Static table with primary and foreign keys
        cur.execute("CREATE TABLE if not exists Static_Data(Station_number INT PRIMARY KEY, Name TEXT, Address TEXT, Latitude REAL, Longitude REAL,  FOREIGN KEY(station_number) REFERENCES Dynamic_Data(station_number))")

    conn.commit() #Commit dtatbase changes
    cur.close()
    conn.close()# Close connection to allow for tables to be created in seperate functions

    #Import static and historical data
    import_static_data(static_data)
    #import_historical_data(data_directory)
    #import_historical_data_files(data_directory_files)

def import_static_data(static_data):
    """
        Function to import static data into static table
        :return: None
    """
    conn = lite.connect('dublinbikes_test_database.db') # Local path to database
    try: # Error checking if there is an error on data insertion should not be necessary at all
        with conn: # Run only if connection is made (optional)

            cur = conn.cursor() # Cursor class which is used to execute SQL statements
            for station_no in range(1,103):
                    if station_no != 50:
                        station_index = static_data[station_no]
                        cur.execute("INSERT OR IGNORE INTO Static_Data(Station_number, Name, Address, Latitude, Longitude) VALUES(?,?,?,?,?)",
                                    (station_index['number'], station_index['name'], station_index['address'], station_index['latitude'], station_index['longitude']))
    except:
        print('Error. Duplicate key for station number' + str(station_no))

def import_historical_data(data_directory):
    """
        Import historical dynamic data. Iterate through json files in sub directory to do so.
        :return: None
    """

    #Obtain list of json files in directory
    dir_files = os.listdir(data_directory)

    #Remove hidden files
    data_files = []
    for file in dir_files:
        if file[0] != '.':
            data_files.append(file)

    #Iterate through Json files
    for json_file in data_files:
        file_path = data_directory + '/' + json_file

        #Open Json file
        with open(file_path) as json_data:
            json_data = (json.load(json_data))

       # Make a connection for each file
        conn = lite.connect('dublinbikes_test_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
        with conn:
            cur = conn.cursor()
            #Open dicitionary in json file and iterate through all stations exlduing 50
            for station_no in range(1,103):
                if station_no != 50:
                    try: #Error checking in case there is a missing station in dataset
                        station_index = json_data[str(station_no)]
                        cur.execute("INSERT OR IGNORE INTO Dynamic_Data(Station_number, Timestamp, Last_update, Weekday, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (station_no, station_index['time_stamp'], station_index['last_update'],station_index['week_day'], station_index['status'], station_index['bike_stands'],station_index['available_bike_stands'],
                                station_index['available_bikes']))
                    except:
                        print("The dataset is missing station number " + str(station_no))
        # Close transaction, commiting changes to database
        conn.commit()
        cur.close()
        conn.close()

def import_historical_data_files(data_directory_files):
    """
        Import historical dynamic data via files method. Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return: None
    """
    #Obtain list of json files in directory
    dir_files = os.listdir(data_directory_files)

    #Remove hidden files
    data_files = []
    for file in dir_files:
        if file[0] != '.':
            data_files.append(file)

    #Iterate through Json files
    for json_file in data_files:
        filename_with_type= json_file.split('_', 2)
        timestamp = filename_with_type[0]
        filename = filename_with_type[1].split('.', 2)
        weekday = filename[0]
        file_path = data_directory_files + '/' + json_file

        #Open Json file
        with open(file_path) as json_data:
            json_data = (json.load(json_data))

       # Make a connection for each file
        conn = lite.connect('dublinbikes_test_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
        with conn:
            cur = conn.cursor()
            #Open dicitionary in json file and iterate through all stations exlduing 50
            for station_no in range(1,103):
                if station_no != 50:
                    try: #Error checking in case there is a missing station in dataset
                        station_index = json_data[str(station_no)]
                        cur.execute("INSERT OR IGNORE INTO Dynamic_Data(Station_number, Timestamp, Last_update, Weekday, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (station_no, timestamp, station_index['last_update'], weekday, station_index['status'], station_index['bike_stands'],station_index['available_bike_stands'],
                                station_index['available_bikes']))
                    except:
                        print("The dataset is missing station number " + str(station_no))
        # Close transaction, commiting changes to database
        conn.commit()
        cur.close()
        conn.close()


def import_dynamic_data(dynamic_data):
    """
        Import dynamic . Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return:
    """
    #Connect to database
    conn = lite.connect('dublinbikes_test_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        for station_no in range(1,103):
            if station_no != 50:
                try:
                    station_index = dynamic_data[station_no]
                    cur.execute("INSERT OR IGNORE INTO Dynamic_Data(Station_number, Timestamp, Last_update, Weekday, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (station_no, station_index['time_stamp'], station_index['last_update'],station_index['week_day'], station_index['status'], station_index['bike_stands'],station_index['available_bike_stands'],
                                station_index['available_bikes']))
                except:
                    print("The dataset is missing station number " + str(station_no))
    conn.commit() #Redundant here
    cur.close()
    conn.close()

if __name__ == '__main__':
    static_data_dict = return_static_data()
    create_database(static_data_dict,'Historical_data/Data','Historical_data/Data_old')
    import_dynamic_data(dynamic_data_dict)
