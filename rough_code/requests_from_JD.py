# Conor O'Kelly


# Small bit of test code to show that API key work and request for Dublin contracts works


import urllib.request as request

key = 'a4dc19867e72bc955aa9a438f2b90a8c7b6067f7l'

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=a4dc19867e72bc955aa9a438f2b90a8c7b6067f7"


file = request.urlopen(url)

print (file.read())
