# Conor O'Kelly


# Small bit of test code to show that API key work and request for Dublin contracts works


import urllib.request as request
import re,json

key_append = '&apiKey=a4dc19867e72bc955aa9a438f2b90a8c7b6067f7'

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin"

specfic_station = "https://api.jcdecaux.com/vls/v1/stations/42?contract=Dublin"


file = request.urlopen(url+key_append).read()
# object = json.loads('{"number":42,"name":"SMITHFIELD NORTH","address":"Smithfield North","position":{"lat":53.349562,"lng":-6.278198},"banking":true,"bonus":false,"status":"OPEN","contract_name":"Dublin","bike_stands":30,"available_bike_stands":24,"available_bikes":6,"last_update":1457002251000}')


file_read = file.decode('UTF-8')
print(file_read.count("number"))
file = (re.findall('\{.*?\}.*?\}', file_read))

dict = json.loads(file_read)

item = dict[0]
print(item)

print(item.get("contract_name"))

