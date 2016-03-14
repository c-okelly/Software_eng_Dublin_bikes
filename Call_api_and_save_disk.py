
import urllib.request as request
import re,json,io
import time

def get_station_data_save_to_json_file():

    key_append = '&apiKey=a4dc19867e72bc955aa9a438f2b90a8c7b6067f7'

    url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin"

    specfic_station = "https://api.jcdecaux.com/vls/v1/stations/42?contract=Dublin"


    file = request.urlopen(url+key_append).read()

     # Concert file to UTF-8
    file_read = file.decode('UTF-8')

    # Use json lib to convert each station info into list of dics => but has no master key
    dict_to_save = json.loads(file_read)

    # Create file name with time stamp and day of the week.
    current_time = time.gmtime()
    time_of_day = (time.strftime("%Y%m%d%H%M", current_time))
    time_of_week = (time.strftime("%a", current_time))
    file_name = (time_of_day + "_" + time_of_week+".json")

    with open(file_name, 'w') as f:
        json.dump(dict_to_save, f, ensure_ascii=False)


def run_once_min():

    while True:
        try:
            get_station_data_save_to_json_file()
            wait_time = (59.75)
            time.sleep(wait_time)
        except:
            current_time = time.gmtime()
            time_of_day = (time.strftime("%Y%m%d%H%M", current_time))
            print("error at %i", time_of_day)
            wait_time = (59)
            time.sleep(wait_time)


if __name__ == '__main__':
    run_once_min()
