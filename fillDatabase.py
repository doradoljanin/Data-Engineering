import pandas as pd
import dbHelper

def convert_date_format(date_str):
   if(len(date_str) == 0): return None
   date_list = date_str.split(".")
   return "{}-{}-{}".format(date_list[2], date_list[1], date_list[0])

# Create a dbHelper object
db_helper = dbHelper.DbHelper(host="localhost", database="playersData", user="postgres", password="bazepodataka", port="5433")

data = pd.read_csv("playersData.csv", sep=";")

selected_columns = ['PlayerID', 'URL', 'Name', 'Full name', 'Date of birth', 'Age', 'City of birth', 'Country of birth', 'Position', 'Current club', 'National_team']
data = data[selected_columns]

# Fill all NaN values with 'Unknown'
data.fillna('', inplace=True)

for col in selected_columns:
   print(col, data[col].duplicated().any())

for index, row in data.iterrows():
   player = {
            "player_id": row['PlayerID'] if row['PlayerID'] else None,
            "url": row['URL'] if row['URL'] else None,
            "name": row['Name'] if row['Name'] else None,
            "full_name": row['Full name'] if row['Full name'] else None,
            "date_of_birth": convert_date_format(row['Date of birth']),
            "age": row['Age'] if row['Age'] else None,
            "place_of_birth": row['City of birth'] if row['City of birth'] else None,
            "country_of_birth": row['Country of birth'] if row['Country of birth'] else None,
            "positions": row['Position'] if row['Position'] else None,
            "current_club": row['Current club'] if row['Current club'] else None,
            "national_team": row['National_team'] if row['National_team'] else None,
            "appearances": None,
            "goals": None,
            "scraping_timestamp": None
        }
   
   db_helper.insert_player(player)

# Close the db connection
db_helper.close()
