
_author__ = "Shane Kenny"

import sqllite_database
import Call_api_and_save_disk


def main():
  "main point of entry for project"

  print('Creating or opening database')
  static_data_dict = sqllite_database.return_static_data()
  sqllite_database.create_database(static_data_dict, 'Historical_data/Data', 'Historical_data/Data_old')
  dynamic_data_dict = sqllite_database.format_station_data('c22c69d2077c8520674a591abf2aaaccbf6e2440')
  sqllite_database.import_dynamic_data(dynamic_data_dict)

  print("Starting regular scrape of dynamic data now")
  Call_api_and_save_disk.run_every_x_minutes()
  Call_api_and_save_disk.return_static_data()




if __name__ == '__main__':
    main()