__author__ = 'Connor Fitzmaurice'


import sqlite3 as lite # Import sql lite support


def create_database():
    """
        Fuction to create database. Calls functions to create tables and import pre-exisitng data
    """
    conn = lite.connect('dublinbike_test_database.db',  isolation_level = None) # connect () works by searching for a database file and connecting to it
    with conn: # Run only if connection is made (optional)
        cur = conn.cursor() # Cursor class which is used to execute SQL statements

        # Create dynamic table
        cur.execute("CREATE TABLE if not exists CREATE TABLE Dynamic_Data(PRIMARY KEY(Station_number INT, Timestamp INT), Last_update REAL, Status TEXT, Bike_stands INT, Available_bike_stands INT, Available_bikes INT)")

        #Create Static table with primary and foreign keys
        cur.execute("CREATE TABLE if not exists Static_Data(station_number INT PRIMARY KEY, Name TEXT, Address TEXT, Latitude REAL, Longtitude REAL  FOREIGN KEY(station_number), REFERENCES Dynamic_Data(station_number))")
    conn.commit()
    cur.close()
    conn.close()# Close connection to allow for tables to be created in seperate functions

    import_static_data()
    #import_historical_data()
    #import_dynamic_data()

def import_static_data():
    """
        Create static data and import data. Currently designed for use with parsed dicitonary of static data with station number as key
        :return: None
    """
    conn = lite.connect('dublinbikes_test_database.db') # connect () works by searching for a database file and connecting to it
    with conn: # Run only if connection is made (optional)
        cur = conn.cursor() # Cursor class which is used to execute SQL statements
        #Static data import
        cur.executemany("INSERT INTO Static_Data(Station_number, Name, Address, Latitude, Longtitude) VALUES('?','?','?','?','?')", superdictionary_stations)

    conn.commit()
    cur.close()
    conn.close



def import_historical_data():
    """
        Import historical dynamic data. Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return: None
    """
    conn = lite.connect('dublinbikes_database.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
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

create_database()