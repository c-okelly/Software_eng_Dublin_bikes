__author__ = 'Connor Fitzmaurice'


import sqlite3 as lite # Import sql lite support

def create_database():
    """
        Fuction to create database. Calls functions to create tables and import pre-exisitng data
    """
    conn = lite.connect('test4.db') # connect () works by searching for a database file and connecting to it
    conn.close()# Close connection to allow for tables to be created in seperate functions
    create_dynamic_table()
    create_static_table()
    import_historical_data()



def create_static_table():
    """
        Create static data and import data. Currently designed for use with parsed dicitonary of static data with station number as key
        :return:
    """
    conn = lite.connect('test4.db') # connect () works by searching for a database file and connecting to it
    with conn: # Run only if connection is made (optional)
        cur = conn.cursor() # Cursor class which is used to execute SQL statements
        #Static data
        cur.execute("CREATE TABLE if not exists Static_Data(station_number INT PRIMARY KEY, Name TEXT, Address TEXT, Latitude REAL, Longtitude REAL  FOREIGN KEY(station_number), REFERENCES Dynamic_Data(station_number))")
        #cur.executemany("INSERT INTO Static_Data(Station_number, Name, Address, Latitude, Longtitude) VALUES('?','?','?','?','?')", station_static['Station_number'], station_static['Name'], station_static['Address'], station_static['Latitude'], station_static['Longtitude'])

    conn.commit()
    cur.close()
    conn.close



def create_dynamic_table():
    """
        Create dynamic data table
        :return:
    """

    conn = lite.connect('test4.db') # connect () works by searching for a database file and connecting to it
    with conn: # Run only if connection is made (optional)
        cur = conn.cursor() # Cursor class which is used to execute SQL statements
        #Dynamic data
        cur.execute("CREATE TABLE if not exists CREATE TABLE Dynamic_Data(PRIMARY KEY(Station_number INT, Timestamp INT), Last_update REAL, Status TEXT, Bike_stands INT, Available_bike_stands INT, Available_bikes INT)")
    conn.commit()
    cur.close()
    conn.close



def import_historical_data():
    """
        Import historical dynamic data. Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return:
    """
    conn = lite.connect('test4.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        cur.executemany("INSERT INTO Dynamic_Data (Station_number, Timestamp, Last_update, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES('?','?','?','?','?','?','?')", [historical_data['Station_number'], historical_data['Timestamp'], historical_data['Last_update'],historical_data['Bike_stands'],historical_data['Available_bike_stands'], historical_data['available_bikes']])
    conn.commit()
    cur.close()
    conn.close()


def import_dynamic_data():
    """
        Import dynamic . Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return:
    """
    #Connect to database
    conn = lite.connect('test4.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        cur.executemany("INSERT INTO Dynamic_Data (station_number, Timestamp, Last_update, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES('?','?','?','?','?','?','?')", [station['Station_number'], station['Timestamp'], station['Last_update'],station['Bike_stands'],station['Available_bike_stands'], station['Available_bikes']])
    conn.commit() #Redundant
    cur.close()
    conn.close()



def database_backup(database, backup):
    """
        Function to backup database
        :return:
    """
    #Backup to sql file
    conn = lite.connect('test4.db')
    with open('test4_backup.sql', 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)

def data_retrieval():
    """
        Fucntion ti query database
        :return:
    """
    # Connect to database
    conn = lite.connect('test4.db',  isolation_level = None) #'Isolation level means that connection is in autocommit mode'
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM Dynamic_Data')

        rows = cur.fetchall()

        for row in rows:
            print(row)
    cur.close()
    conn.close()
