
_author__ = "Shane Kenny"


import urllib
import Call_api_and_save_disk
import sqllite_database




def main():
  "main point of entry for project"
  sqllite_database()
  #call sql database creation py file.
  Call_api_and_save_disk()
  # call scrape and update file.




if __name__ == '__main__':
    main()