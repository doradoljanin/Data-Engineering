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

## Description

### playersScraper.py:

This file contains the main logic for scraping the data from the player URLs, parsing the HTML pages, and storing the data into the PostgreSQL database. It also handles updating existing players in the database.

### dbHelper.py:

This file contains the functions for performing database operations such as connecting to the database, creating tables, inserting data, and querying data.

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
3. Enrich all players' data with columns AgeCategory and GoalsPerClubGame by executing the following command::
4. Calculate the average age, the average number of appearances and the total number of players by club
5. extract the number of players who are younger, play in the same position and have a
   higher number of current club appearances for every player from one chosen club
