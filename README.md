City Biking Station Interface 

Contributors:

Connor Fitzmaurice
Shane Kenny
Conor O' Kelly

The goal of this program is to provide a web based interface to users through which they can determine available bike and available bike stands for stations at the current time or at at given historical timestamp. It will try to predict the chances of bikes and stands being available in stations by providing hourly averages.  It does so using data collected at a frequency of 1 minute via an Amazon web instance, for the period of 9th March to 20th April.


CONTENTS OF THIS FILE
---------------------
   
 * Introduction
 * Requirements
 * Recommended modules
 * Installation
 * Running the program
 * Configuration
 * FAQ
 
Introduction
--------------------
 
 
The 'City Biking Station Interface' program displays a website which allows user to query live, historical and hourly averages for stations' available bikes and stands using data stored in the SQLite database where averages for number of available bikes and available stands are calculated and recorded. It does so using data collected at a frequency of 1 minute via an Amazon web instance, for the period of 9th March to 20th April.

![Alt text](/ReadmeImages/WebsiteMockup.png?raw=true "Website Mockup")


The 'City Biking Station Interface' program is designed with robustness and modularity in mind. As such, while currently in use with the JCDeaux API for the Dublin Bikes scheme, it can be adapted to work with other city bike schemes which use the JCDeaux API. It also currently provides data collected during a defined period. With moderate adjustments and hardware support, the 'City Biking Station Interface' can be adapted to run in a live state with data constantly being collected and the hourly averages for stations being recalculated. This would have applications such as users wanting to see how bike usage is impacted by factors such as seasons, bank holidays or price hikes.

* For a full description of the module, visit the project page:
https://github.com/c-okelly/Software_eng_Dublin_bikes.git

* To submit bug reports and feature suggestions, or to track changes:
https://github.com/c-okelly/Software_eng_Dublin_bikes.git
   
Requirements
--------------------

This module requires the following modules:

*   Python 3.X https://www.python.org/downloads/
*   Flask framework version 0.10.1 https://pypi.python.org/pypi/Flask
*   SQLite to connect the web application to the database https://www.sqlite.org/download.html
*   JSON module for parsing data https://pypi.python.org/pypi/simplejson/
*   Nose2 for testing https://github.com/nose-devs/nose2

RECOMMENDED MODULES
----------------------

*   Python 3.5.0 https://www.python.org/downloads/release/python-350/


INSTALLATION
-----------------
* 	Excluding the above packages no more packages/modules need to be installed. All is required is that the dublin_bikes.html is ran to instanciate the flask app, collect data and provide it to the user.


* 	To adjusted the program to work with other cities which use the JCDeaux Api, /modules/Call_api_and_save_disk.py change contract in url "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin" to city required. Also change Station_no range for city in /modules/insert_dynamic_data.py and /modules/sqllite_database.py to correct number for city requested:

-     def get_station_data(api_key):
         key_append = '&apiKey=' + api_key
         url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin"
         current_json_file = request.urlopen(url+key_append).read()
         current_json_file = current_json_file.decode("UTF-8")
         return current_json_file
-     for station_no in range(1,103):
                if station_no != 50:

* 	To have the map on the bikes_html page show the correct location change the variable “focus_city_coordinates = [lat, long]” in bikes.js line 1 to the latitude and longitude of the required city.

*  To adjust the program to run in a live state import and instantiate function /modules/sqlite_database_queries.py.update_averages() run daily. This will update the hourly average table as more data is collected.


Running the program
-----------------
* 	To run the program just complete the following steps.

	1. Run master.py. 	
	This will generate current data by calling from the the api.

	2. Run app.py.		
	This will launch flask and have a server ready for date request from the webpage

	3. Open dublin_bikes.html and make the required request.


CONFIGURATION
-----------------
* 	To run the City Biking Station Interface in its current format, no configuration is required

* 	Select the request type via the uses of checkboxes and historical and hourly data for dropdown boxes for year, month, day, hour minute and  day of the week and hour respectively

* 	To change the range of available data in the database change the variable “database_range = [start, finish]” on line 4 in bikes.js

![Alt text](/ReadmeImages/1.png?raw=true "Website Image")

* 	This information will be displayed via a map interface. 


TROUBLESHOOTING
-----------------

*   For any difficulties in displaying the interface check the following:
    - All files for the webisite are in the correct folder
    - Update browser if your version is old
    - Run webpage in case issue is browser specific.
*   For difficulties connecting to database ensure file path to database is correct. If difficulties persists, run sqllite_database as a main to create a local database.


FAQ
-----------------

Q: 	What do the three colors for the markers on the map mean?

A: 	Each marker is a station station. The color indicates percentage of bikes available.   
-Red Color: Less than 20% of bikes available for hire.  
-Yellow Color: Between 20% and 60% of bikes available for hire.  
-Green Color:  More than 60% of bikes available for hire.  

----------------------------------------------------------------------------------------------------------
Q:	Why is your data only limited to between the 9th of March and 20th April?

A:	The data which is used by the interface was collected over this period. If the data collection is configured to run live, this range can be expanded forward. 

