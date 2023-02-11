import psycopg2
from psycopg2 import Error

# A class for connecting to a PostgreSQL database using the psycopg2 library
class DbHelper:
   def __init__(self, host, database, user, password, port):
      self.conn = psycopg2.connect(
         host=host,
         database=database,
         user=user,
         password=password,
         port=port
      )
      self.cur = self.conn.cursor()

   def close(self):
      self.conn.close()

   # Returns True if player with the given url already exists in the database, False otherwise
   def check_player_exists(self, player_url):
      cur = self.conn.cursor()
      cur.execute("SELECT 1 FROM players WHERE url = %s", (player_url,))
      return cur.fetchone() is not None

   # Gets All Players Data
   def getAllPlayersData(self):
      results = None
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # execute the query
         cur.execute("SELECT * FROM players;")

         # Fetch the results
         results = cur.fetchall()

         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while selecting all players data: {error}")
         self.conn.rollback()

      finally:
         cur.close()
         return results

   # Updates an existing player in the database with the updated player_data
   def update_player(self, player_data):
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # create an update query
         update_query = """
            UPDATE players
            SET name = %s, full_name = %s, date_of_birth = %s, age = %s, place_of_birth = %s, country_of_birth = %s, positions = %s, 
                  current_club = %s, national_team = %s, num_appearances_curr_club = %s, goals_curr_club = %s, scraping_timestamp = %s
            WHERE url = %s
         """

         # execute the query
         cur.execute(update_query, (
            player_data.get('name'),
            player_data.get('full_name'),
            player_data.get('date_of_birth'), 
            player_data.get('age'),
            player_data.get('place_of_birth'),
            player_data.get('country_of_birth'),
            player_data.get('positions'),
            player_data.get('current_club'),
            player_data.get('national_team'),
            player_data.get('appearances'),
            player_data.get('goals'),
            player_data.get('scraping_timestamp'),
            player_data.get('url')
         ))
         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while updating player data: {error}")
         self.conn.rollback()

      finally:
         cur.close()

   # Inserts a new player into the database
   def insert_player(self, player_data):
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # create an INSERT query
         insert_query = """
            INSERT INTO players (player_id, url, name, full_name, date_of_birth, age, place_of_birth, 
            country_of_birth, positions, current_club, national_team, num_appearances_curr_club, goals_curr_club, scraping_timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """

         # execute the query
         cur.execute(insert_query, (
            player_data.get('player_id'),
            player_data.get('url'),
            player_data.get('name'),
            player_data.get('full_name'),
            player_data.get('date_of_birth'), 
            player_data.get('age'),
            player_data.get('place_of_birth'),
            player_data.get('country_of_birth'),
            player_data.get('positions'),
            player_data.get('current_club'),
            player_data.get('national_team'),
            player_data.get('appearances'),
            player_data.get('goals'),
            player_data.get('scraping_timestamp')
         ))

         # commit the changes
         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while inserting player data: {error}")
         self.conn.rollback()

      finally:
         cur.close()

   # Adds the AgeCategory column
   def addAgeCategory(self):
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # create an update query
         query = """
            ALTER TABLE players ADD COLUMN age_category varchar(10);

            UPDATE players
            SET age_category =
               CASE 
                  WHEN age <= 23 THEN 'Young'
                  WHEN age BETWEEN 24 AND 32 THEN 'MidAge'
                  WHEN age >= 33 THEN 'Old'
                  ELSE NULL
               END;
         """

         # execute the query
         cur.execute(query)
         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while setting age_category column: {error}")
         self.conn.rollback()

      finally:
         cur.close()

   # Adds the GoalsPerClubGame column
   def addGoalsPerClubGame(self):
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # create an update query
         query = """
            ALTER TABLE players ADD COLUMN goals_per_club_game float;

            UPDATE players SET goals_per_club_game = 
               CASE
                  WHEN goals_curr_club IS NULL OR num_appearances_curr_club IS NULL OR num_appearances_curr_club = 0 THEN NULL
                  ELSE goals_curr_club / num_appearances_curr_club
               END;
         """

         # execute the query
         cur.execute(query)
         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while setting goals_per_club_game column: {error}")
         self.conn.rollback()

      finally:
         cur.close()

   # Gets Avg Age, Avg Appear and Total Number of Players By Club
   def getAvgAgeAppearTotalPlayersByClub(self):
      results = None
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # create an update query
         query = """
            SELECT 
               current_club, 
               AVG(age) as avg_age, 
               AVG(num_appearances_curr_club) as avg_appearances, 
               COUNT(player_id) as total_players
            FROM 
               players
            GROUP BY 
               current_club;
         """

         # execute the query
         cur.execute(query)

         # Fetch the results
         results = cur.fetchall()

         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while getting AvgAgeAppearTotalPlayersByClub: {error}")
         self.conn.rollback()

      finally:
         cur.close()
         return results

   # Gets Younger Players on the Same Position with More Appearances for every player in the specified club
   def getYoungerSamePositionMoreAppearances(self, club_name):
      results = None
      try:
         # create a cursor object
         cur = self.conn.cursor()

         # create an update query
         query = """
            WITH club_players AS (
               SELECT name, date_of_birth, positions, num_appearances_curr_club
               FROM players
               WHERE current_club = %s
            )
            SELECT name,
               (SELECT COUNT(*) 
               FROM players 
               WHERE positions = club_players.positions 
                  AND num_appearances_curr_club > club_players.num_appearances_curr_club 
                  AND date_of_birth > club_players.date_of_birth) 
               AS count_younger_same_pos_more_app
            FROM club_players;
         """

         # execute the query
         cur.execute(query, (club_name,))

         # Fetch the results
         results = cur.fetchall()

         self.conn.commit()

      except (Exception, psycopg2.DatabaseError) as error:
         print(f"Error while getting YoungerSamePositionMoreAppearances: {error}")
         self.conn.rollback()

      finally:
         cur.close()
         return results