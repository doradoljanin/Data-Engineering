# Data-Engineering Task

## Introduction

This repository contains a solution for a simple web scraper that scrapes data from the specified website and stores it in a SQL Database. It enables additional queries for enriching the data and calculating specific metrics. The solution is implemented using the Python programming language and the PostgreSQL database.

## Requirements

* Python 3.x
* Required Python libraries:
  * pandas
  * psycopg2
  * requests
  * beautifulsoup4

## Description of the solution

#### dbHelper.py:

This file contains the functions for performing database operations such as connecting to the database, creating tables, inserting data, updating data and querying data.

#### fillDatabase.py

This script imports the initially delivered data (playersData.csv) into the SQL database by calling dbHelper's functions.

#### playersScraper.py:

This file contains the main logic for scraping the data from the players' URLs, parsing the HTML pages, and calling dbHelper to insert or update the data in the PostgreSQL database. Additionally, it saves the resulting data table to the players_data_scraped.csv file.

#### enrichDataWithAgeCategoryAndGoalsPerGame.py

This script calls a dbHelper's function which enriches players' data by adding two new columns: AgeCategory (string) and GoalsPerClubGame (float). The results are saved to the players_data_enriched.csv file.

#### avgAgeAppearTotalPlayersByClub.py

This script calls a dbHelper's function which executes a query for calculating the average age, the average number of appearances and the total number of players by club. The results are saved to the avg_age_appearances_total_players.csv file.

#### youngerSamePositionMoreAppearances.py

This script calls a dbHelper's function which executes a query that will do the following: for every player from one chosen club, extract the number of players who are younger, play in the same position and have a higher number of current club appearances than that player. The results are saved to the younger_same_pos_more_app.csv file. 

## Installation

1. Clone the repository to your local machine.

```
git clone https://github.com/doradoljanin/Data-Engineering.git
```

2. Install the required libraries by running:

```
pip install -r requirements.txt
```

## Usage

1. Import the initially delivered data (playersData.csv) into the SQL database by executing the following command:

```
python fillDatabase.py playersData.csv
```

2. Import the scraped data into the SQL database by executing the following command:

```
python playersScraper.py playersURLs.csv
```

3. Enrich players' data with columns AgeCategory (string) and GoalsPerClubGame (float) by executing the following command:

```
python enrichDataWithAgeCategoryAndGoalsPerGame.py
```

4. Calculate the average age, the average number of appearances and the total number of players by club by executing the following command:

```
python avgAgeAppearTotalPlayersByClub.py
```

5. Extract the number of players who are younger, play in the same position and have a higher number of current club appearances than that player for every playerfrom one chosen club (*club_name*). The script `youngerSamePositionMoreAppearances.py` requires a single argument, `club_name`, which specifies the name of the club for which you want to find players with a younger age and more appearances than the average for that club.
   ```
   python youngerSamePositionMoreAppearances.py Liverpool club_name
   ```

   * For example, if you want to extract data for Liverpool, you should run the script as follows:

```
        python youngerSamePositionMoreAppearances.py Liverpool
