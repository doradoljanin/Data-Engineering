import csv
import requests
from bs4 import BeautifulSoup
import dbHelper
import sys
import re
import pandas as pd

def only_letters(string):
    return re.sub(r'[^a-zA-Z]+', '', string)

# Create a dbHelper object
db_helper = dbHelper.DbHelper(host="localhost", database="playersData", user="postgres", password="bazepodataka", port="5433")

players_url_file = sys.argv[1]

# Read the player URLs from the CSV file
with open(players_url_file, 'r') as file:
    reader = csv.reader(file)
    player_urls = list(reader)

# Scrape data for each player URL
for player_url in player_urls:
    player_url = player_url[0]

    # Send an HTTP request to the URL
    response = requests.get(player_url)

    # Check if the request was successful
    if response.status_code == 200:
        # parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')

        player_id = None

        try: name = soup.find("caption", {"class": "infobox-title fn"}).text
        except: continue

        try: full_name = soup.find("td", {"class": "infobox-data nickname"}).next[1:]
        except: full_name = None

        try: date_of_birth = soup.find("span", {"class": "bday"}).text
        except: date_of_birth = None

        try: 
            age = soup.find("span", {"class": "noprint ForceAgeToShow"}).text
            age = int(age.split()[1][:-1])
        except: age = None

        try:
            place = soup.find("td", {"class": "infobox-data birthplace"}).text
            places = place.split(", ")
            places = [only_letters(place) for place in places]
            # extract place of birth and country of birth
            place_of_birth = places[0]
            country_of_birth = places[-1]
        except:
            place_of_birth = None
            country_of_birth = None

        try: positions = soup.find("td", {"class": "infobox-data role"}).next_element.next_element.text
        except: positions = None

        try: current_team = soup.find("td", {"class": "infobox-data org"}).text[1:] 
        except: current_team = None

        try:
            teams = soup.find_all('td', class_='infobox-data-a')
            national_team = teams[-1].text[1:]
        except: national_team = None

        try: num_appearances_curr_club = int(next(team.find_next('td', class_='infobox-data-b').text[1:] for team in teams if team.text[1:] == current_team))
        except: num_appearances_curr_club = None

        try: goals_curr_club = int(next(team.find_next('td', class_='infobox-data-c').text[2:-1] for team in teams if team.text[1:] == current_team))
        except: goals_curr_club = None

        # Fill in the extracted information into a dictionary
        player = {
            "player_id": player_id,
            "url": player_url,
            "name": name,
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "age": age,
            "place_of_birth": place_of_birth,
            "country_of_birth": country_of_birth,
            "positions": positions,
            "current_club": current_team,
            "national_team": national_team,
            "appearances": num_appearances_curr_club,
            "goals": goals_curr_club,
            "scraping_timestamp": 'now()'
        }
        
        # Check if the player information for the given URL already exists in the database
        player_exists = db_helper.check_player_exists(player_url)

        if player_exists is None: break

        # Update the existing player information if it exists, otherwise insert as a new record
        if player_exists:
            db_helper.update_player(player)
        else:
            db_helper.insert_player(player)
    else:
        print("Failed to retrieve the page")

    # Fetch the results
    results = db_helper.getAllPlayersData()

    # Create a DataFrame from the results
    df = pd.DataFrame(results, columns=["id", "player_id", "url", "name", "full_name", "date_of_birth", "age", "place_of_birth", 
                "country_of_birth", "positions", "current_club", "national_team", "num_appearances_curr_club", "goals_curr_club", 
                "scraping_timestamp"])

    df.to_csv('players_data_scraped.csv', index=False)


# Close the db connection
db_helper.close()