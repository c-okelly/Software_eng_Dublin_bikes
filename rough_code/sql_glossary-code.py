__author__ = 'Connor Fitzmaurice'
# Import sql lite
import sqlite3 as lite
import sys

# Check version of sqlite
lite.version
# Check libray sqlite is working with
lite.sqlite_version



# Database creation function

#Create database or connect to existing one. If database not found it, it creates a fresh database with name given
# This can be used as part of the check to see if the database exists alongside other things such as try clause
conn = lite.connect('test.db') # connect () works by searching for a database file and connecting to it

cur = conn.cursor() # Cursor class which is used to execute SQL statements



#Table Creation

# Create static_data table
with conn: # Run only if connection is made (optional)
    cur = conn.cursor()
    cur.execute("CREATE TABLE Static_Data(station_number INT PRIMARY KEY, Name TEXT, Address TEXT, Latitude INT, Longtitude INT)")

# Create dynamice_data table
with conn: # Run only if connection is made (optional).
    c = conn.cursor()
    cur.execute("CREATE TABLE Dynamic_Data(PRIMARY KEY(station_number INT, Timestamp INT), Last_Update INT, Status TEXT, Bike_stands INT, Available_Bike_stands INT, Available_Bikes INT)")




# Data Insertion

# Method by which to insert python lists into table

example_dictionary = ((data row here))

#Connect to database
# Try clause to provide for fault tolerance when inserting dynamic data into database table
try:
    conn = lite.connect('test.db' isolation_level = None) 'Isolation level means that connection is in autocommit mode'
    with conn:
        c = conn.cursor()
        cur.execute("INSERT INTO Cars VALUES(?, ?, ?)", example_dictionary)

# Try and error clause to provide for fault toleranceE when inserting data
# #try:

#except lite.Error, e:
#    if conn:
#       conn.rollback() # Data rolled back if errors occurs
#       print "Error %s:" % e.args[0]
# sys.exit(1)



# Data Integrity

# Data collected can be dumped to file for backup
# Done by table
def writeData(data):

    f = open('static_data.sql', 'w')

    with f:
        f.write(data)

con = lite.connect('test.db')

with con:

    cur = con.cursor()

    data = '\n'.join(con.iterdump())

    writeData(data)
