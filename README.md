# Data-Engineering
This repository contains a solution for a simple web scraper that scrapes data from the specified website and stores it in the SQL Database. It enables additional queries for enriching the data and calculating specific metrics.

By installing these packages with pip install -r requirements.txt, you will be able to run the web scraper code on your computer.

This solution has two .py files:

playersScraper.py: This file contains the main logic for scraping the data from the player URLs, parsing the HTML pages, and storing the data into the PostgreSQL database. It also handles updating existing players in the database.

dbHelper.py: This file contains the functions for performing database operations such as connecting to the database, creating tables, inserting data, and querying data.

To run the scraper script from the command line using the playersURLs.csv file as an argument, run 'python playersScraper.py playersURLs.csv'.

Note: napraviti da se username i password za posgresql bazu podataka primaju kao argumenti? - za testni zadatak ne treba