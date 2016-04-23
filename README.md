City Biking Station Interface 

Contributors:

Connor Fitzmaurice
Shane Kenny
Conor O' Kelly

The goal of this program is to provide an web based interface to users through which they can determine available bike and available bike stands for stations at the current time or at at given historical timestamp. It will provide predict the chances of bikes and stands being available in stations. It does so using data collected at a frequency of 1 minute via an Amazon web instance, for the period of 9th March to 20th April. This data is stored in an SQLite database where averages for number of available bikes and available stands are calculated and recorded. This allows users to use the program to see what station are likely to have bikes to rent or stands available based off information provided via a live data call or hourly average.

The 'City Biking Station Interface' program is designed with robustness and modularity in mind. As such, while currently in use with the JCDeaux API for the Dublin Bikes programme, it can be adapted to work with other city bike schemes which are managed using the JCDeaux. It also currently provides data collected during a defined period. With moderate adjustments and hardware support, the 'City Biking Station Interface' can be adapted to run in a live state with data constantly being collected and the hourly averages for stations being recalculated. This would have applications such as users wanting to see how the Bike scheme is impacted by factors such as seasons, bank holidays or price hikes.

CONTENTS OF THIS FILE
---------------------
   
 * Introduction
 * Requirements
 * Recommended modules
 * Installation
 * Configuration
 * FAQ
 * Maintainers
