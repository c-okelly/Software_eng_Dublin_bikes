
_author__ = "Shane Kenny"

import sqllite_database
import Call_api_and_save_disk
import insert_dynamic_data


def main():
  "main point of entry for project"

  print('Creating or opening database')
  static_data_dict = Call_api_and_save_disk.return_static_data()
  sqllite_database.create_database(static_data_dict, 'Historical_data/Data', 'Historical_data/Data_old')
  dynamic_data_dict = Call_api_and_save_disk.format_station_data('c22c69d2077c8520674a591abf2aaaccbf6e2440')
  sqllite_database.import_dynamic_data(dynamic_data_dict)

  # New function to run every minute that saves json to file and updates db
  print("Starting regular scrape of dynamic data now")
  insert_dynamic_data.run_every_x_minutes_database("dublinbikes_test_database.db")




if __name__ == '__main__':
    main()