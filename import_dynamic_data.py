import sqlite3 as lite # Import sql lite support
import urllib.request as request
import json
import time
import os

def run_every_x_minutes_database(database_path, data_directory, repeat_every_x_mins=1):

    # Set wait time to x mins mins 0.25 seconds to account for program run time.
    wait_time = ((60 * repeat_every_x_mins)-0.25)

    try:
    	latest_dynamic_data = time_stamp_and_save_api_call_to_file()
        import_dynamic_data(database_path, latest_dynamic_data)
        time.sleep(wait_time)
    except:
        print("Error Importing data")
        time.sleep(15)

def import_dynamic_data(database_path, dynamic_data):
    """
        Import dynamic . Currently designed for use with parsed dicitonary of dynamic data with station number and timestamp as key
        :return:
    """
    #Connect to database
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        for station_no in range(1,103):
            if station_no != 50:
                try:
                    station_index = dynamic_data[station_no]
                    print("loop1", station_index)
                    #print('\n')
                    print(station_no)
                    cur.execute("INSERT OR IGNORE INTO Dynamic_Data(Station_number, Timestamp, Last_update, Weekday, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                               (station_no, station_index['time_stamp'], station_index['last_update'],station_index['week_day'], station_index['status'], station_index['bike_stands'],station_index['available_bike_stands'],
                              station_index['available_bikes']))
                    #cur.execute("INSERT OR IGNORE INTO Dynamic_Data(Station_number) VALUES(?)", (station_no))
                except:
                    print("The dataset is missing station number " + str(station_no))
    conn.commit() #Redundant here
    cur.close()
    conn.close()
