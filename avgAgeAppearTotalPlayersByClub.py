import dbHelper
import pandas as pd

# Create a dbHelper object
db_helper = dbHelper.DbHelper(host="localhost", database="playersData", user="postgres", password="bazepodataka", port="5433")

# Fetch the results
results = db_helper.getAvgAgeAppearTotalPlayersByClub()

if results is not None:
   # Create a DataFrame from the results
   df = pd.DataFrame(results, columns=['current_club', 'avg_age', 'avg_appearances', 'total_players'])

   # Display the DataFrame
   pd.options.display.max_columns = 5
   print(df)

# Close the db connection
db_helper.close()