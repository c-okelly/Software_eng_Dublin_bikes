import sqlite3 as lite # Import sql lite support
import urllib.request as request
import json
import time
import os


def run_every_x_minutes_database(database_path, data_directory, repeat_every_x_mins=1):

    # Set wait time to x mins mins 0.25 seconds to account for program run time.
    wait_time = ((60 * repeat_every_x_mins)-0.25)

    try:
        import_dynamic_data(database_path, data_directory)
        time.sleep(wait_time)
    except:
        print("Error Importing data")
        time.sleep(15)

def import_dynamic_data(database_path,data_directory):
    """
        Import dynamic data. Iterate through first json file in sub directory to do so.
        :return: None
    """

    # Obtain list of json files in directory
    dir_files = os.listdir(data_directory)

    # Remove hidden files
    data_files = []
    for file in dir_files:
        if file[0] != '.':
            data_files.append(file)
    data_files.reverse()
    print(data_files[:])
    # Iterate through Json files
    for json_file in range(1):
        file_path = data_directory + '/' + data_files[json_file]

        # Open Json file
        with open(file_path) as json_data:
            json_data = (json.load(json_data))

        conn = lite.connect(database_path)
        with conn:
            cur = conn.cursor()
            # Open dicitionary in json file and iterate through all stations exlduing 50
            for station_no in range(1, 103):
                if station_no != 50:
                    #try:  # Error checking in case there is a missing station in dataset
                    station_index = json_data[str(station_no)]
                    cur.execute(
                        "INSERT OR IGNORE INTO Dynamic_Data(Station_number, Timestamp, Last_update, Weekday, Status, Bike_stands, Available_bike_stands, Available_bikes) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                        (station_no, station_index['time_stamp'], station_index['last_update'],
                         station_index['week_day'], station_index['status'], station_index['bike_stands'],
                         station_index['available_bike_stands'],
                         station_index['available_bikes']))
                    #except:
                     #   print("The dataset is missing station number " + str(station_no))
        # Close transaction, commiting changes to database
        conn.commit()
        cur.close()
        conn.close()
