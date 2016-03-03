# Conor O'Kelly


# Small bit of test code to show that API key work and request for Dublin contracts works


import urllib.request as request
import re,json

key_append = '&apiKey=a4dc19867e72bc955aa9a438f2b90a8c7b6067f7'

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin"

specfic_station = "https://api.jcdecaux.com/vls/v1/stations/42?contract=Dublin"


file = request.urlopen(url+key_append).read()

# Concert file to UTF-8
file_read = file.decode('UTF-8')

# Use re to convert to list of lists
file = (re.findall('\{.*?\}.*?\}', file_read))

# Use json lib to convert each station info into list of dics => but has no master key
dict = json.loads(file_read)
# print(dict[0])
# print(dict[0].get("number"))

station_data = {}

# Convert items into dict that can be called by station number. Each contains a dict of the relevent station data
for item in dict:
    key = item.get("number")
    station_data.update({key:item})

#Example => station 42. Must call using int not string
print(station_data.get(42))
