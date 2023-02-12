import dbHelper
import pandas as pd
import sys

# Create a dbHelper object
db_helper = dbHelper.DbHelper(host="localhost", database="playersData", user="postgres", password="bazepodataka", port="5433")

club_name = str(sys.argv[1])

# Fetch the results
results = db_helper.getYoungerSamePositionMoreAppearances(club_name)

if results is not None:
   # Create a DataFrame from the results
   df = pd.DataFrame(results, columns=['name', 'count_younger_same_pos_more_app'])

   df.to_csv('younger_same_pos_more_app.csv', index=False)

# Close the db connection
db_helper.close()