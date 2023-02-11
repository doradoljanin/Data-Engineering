import dbHelper
import pandas as pd

# Create a dbHelper object
db_helper = dbHelper.DbHelper(host="localhost", database="playersData", user="postgres", password="bazepodataka", port="5433")

# Add the AgeCategory column
db_helper.addAgeCategory()

# Add the GoalsPerClubGame column
db_helper.addGoalsPerClubGame()

# Fetch the results
results = db_helper.getAllPlayersData()

# Create a DataFrame from the results
df = pd.DataFrame(results, columns=["id", "player_id", "url", "name", "full_name", "date_of_birth", "age", "place_of_birth", 
            "country_of_birth", "positions", "current_club", "national_team", "num_appearances_curr_club", "goals_curr_club", 
            "scraping_timestamp", "age_category", "goals_per_club_game"])

# Display the DataFrame
pd.options.display.max_columns = 20
print(df)

# Close the db connection
db_helper.close()