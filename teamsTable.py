import requests
import mysql.connector
from bs4 import BeautifulSoup

url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"

teams = requests.get(url).json()["teams"]


mydb = mysql.connector.connect(host = "127.0.0.1", 
                                user = "user", 
                                passwd="password1!")

cursor = mydb.cursor()
cursor.execute("USE MLB_GAMES;")
cursor.execute("""
    CREATE TABLE mlb_teams (
    team_ID INT,
    team_name VARCHAR(255),
    division VARCHAR(255),
    conference VARCHAR(255)
    )
    """)
    
for team in teams:
    id = team["id"]
    name = team["name"]
    conference = team["league"]["name"]
    division = team["division"]["name"]
    cursor.execute("""
        INSERT INTO mlb_teams (team_ID, team_name, division, conference)
        VALUES (%s, %s, %s, %s)
        """, (id, name, division, conference))

mydb.commit()
cursor.close()
mydb.close()
