# Conor O'Kelly


# Small bit of test code to show that API key work and request for Dublin contracts works


import urllib.request as request
import re,json

def get_station_data():

    key_append = '&apiKey=a4dc19867e72bc955aa9a438f2b90a8c7b6067f7'

    url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin"

    specfic_station = "https://api.jcdecaux.com/vls/v1/stations/42?contract=Dublin"


    file = request.urlopen(url+key_append).read()

    # Concert file to UTF-8
    file_read = file.decode('UTF-8')

    # # Use re to convert to list of lists
    # file = (re.findall('\{.*?\}.*?\}', file_read))

    # Use json lib to convert each station info into list of dics => but has no master key
    dict_time_stamped = json.loads(file_read)
    # print(dict[0])
    # print(dict[0].get("number"))

    station_data = {}

    # Convert items into dict that can be called by station number. Each contains a dict of the relevent station data
    for item in dict_time_stamped:
        key = item.get("number")
        sub_dict = {}

        station_data.update({key:item})

    """
    Could trim data at this point to refine for database
    Keep => last_update / status / Bike_stands / availibe_bike_stand / availiabe bikes

    """

    #Example => station 42. Must call using int not string
    # print(station_data.get(42))

    return station_data


if __name__ == '__main__':
    file = get_station_data()
    print(file.get(42))
    for i in file.get(42):
        print(i)