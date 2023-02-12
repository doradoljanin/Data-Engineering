import dbHelper
import pandas as pd

# Create a dbHelper object
db_helper = dbHelper.DbHelper(host="localhost", database="playersData", user="postgres", password="bazepodataka", port="5433")

# Fetch the results
results = db_helper.getAvgAgeAppearTotalPlayersByClub()

if results is not None:
   # Create a DataFrame from the results
   df = pd.DataFrame(results, columns=['current_club', 'avg_age', 'avg_appearances', 'total_players'])

   df.to_csv('avg_age_appearances_total_players.csv', index=False)

# Close the db connection
db_helper.close()