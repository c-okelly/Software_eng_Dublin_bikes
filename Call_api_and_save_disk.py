#Author = Conor O'Kelly

import urllib.request as request
import json
import time
import os

# Created exception if user tries to run caller function less then one min
class Run_time_to_short(Exception):
    pass

def get_station_data(api_key):

    # API Key
    key_append = '&apiKey=' + api_key
    # Url for bikes live data
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin"

    #Request and get json file
    current_json_file = request.urlopen(url+key_append).read()

    # Convert file to UTF-8
    current_json_file = current_json_file.decode("UTF-8")

    return current_json_file

def format_station_data(api_key):

    json_file = get_station_data(api_key)

    # Convert each station to a list of dicts
    dict_to_save = json.loads(json_file)

    # All station data
    station_data = {}

    # Create time varialbes
    current_time = time.gmtime()
    time_of_day = (time.strftime("%Y%m%d%H%M", current_time))
    time_of_week = (time.strftime("%a", current_time))
    time_dict = {"time_stamp":time_of_day,"week_day":time_of_week}

    # Convert items into dict that can be called by station number. Each contains a dict of the relevent station data
    for item in dict_to_save:
        key = item.get("number")
        sub_dict = {k: item[k] for k in ('last_update', 'status','bike_stands','available_bike_stands','available_bikes')}
        sub_dict.update(time_dict)
        station_data.update({key:sub_dict})

    # print(station_data.get(2))

    return station_data

def time_stamp_and_save_api_call_to_file(api_key="a4dc19867e72bc955aa9a438f2b90a8c7b6067f7",directory_to_save_to="Data/"):

    station_dicts = format_station_data(api_key)

    # Create file name with time stamp and day of the week.
    current_time = time.gmtime()
    time_of_day = (time.strftime("%Y%m%d%H%M", current_time))
    time_of_week = (time.strftime("%a", current_time))
    file_name = (time_of_day + "_" + time_of_week + ".json")

    # Check data directory exists
    if not os.path.exists(directory_to_save_to):
        os.makedirs(directory_to_save_to)

    # Save in data directory
    file_name = directory_to_save_to + file_name

    # Add time stamp into every sub dictionary
    # for dict in


    # Save Json file.
    with open(file_name, 'w') as f:
        json.dump(station_dicts, f, ensure_ascii=False)

    return station_dicts

def run_every_x_minutes(repeat_every_x_mins=1,api_key="a4dc19867e72bc955aa9a438f2b90a8c7b6067f7",directory_to_save_to="Data/"):
    #Defualt API key is set. Can also insert argument to use an alternative one.
    #Defualt runtime set. Can change to another runtime. Minimum one minute.

    # Raise run time error if under 1 min.
    if repeat_every_x_mins < 1:
        raise Run_time_to_short

    # Set wait time to x mins mins 0.25 seconds to account for program run time.
    wait_time = ((60 * repeat_every_x_mins)-0.25)

    # Create loop to run indefinitely
    while True:
        try:
            time_stamp_and_save_api_call_to_file(api_key,directory_to_save_to)
            time.sleep(wait_time)
        except:
            current_time = time.gmtime()
            time_of_day = (time.strftime("%Y%m%d%H%M", current_time))
            time_of_week = (time.strftime("%a", current_time))
            print("An error occured at %s on %s" % (time_of_day,time_of_week))
            # Wait 15 seconds before restarting
            time.sleep(15)

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

if __name__ == '__main__':
    # Three main functions.

    # print(time_stamp_and_save_api_call_to_file())
    print("Starting")
    run_every_x_minutes()
    # return_static_data()
    print("Functions are comment out")
