import mysql.connector
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import json

team_records = {}
def calculateStandings(year):
    delta = timedelta(days=1)
    startDate = date(year, 1, 1)
    endDate = date(year, 12, 31)
    while startDate <= endDate:
        dateString = startDate.strftime("%Y-%m-%d")
        calculateRecord(dateString)
        startDate += delta

def calculateRecord(date):
    mydb = mysql.connector.connect(host = "127.0.0.1", 
                                user = "user", 
                                passwd="password1!")
    cursor = mydb.cursor()
    cursor.execute("USE MLB_GAMES;")
    cursor.execute("""
    SELECT *
    FROM mlb_games
    WHERE date = %s
    """, (date,))
    result = cursor.fetchall()
    for game in result:
        if(game[11] != "Regular Season"):
           continue
        home_team_name = game[3]
        home_team_id = game[4]
        away_team_name = game[5]
        away_team_id = game[6] 
        if home_team_id not in team_records:
            team_records[home_team_id] = {
            "name": home_team_name,
            "conference": "",
            "division": "",
            "wins": 0,
            "losses": 0,
            "runs_scored": 0,
            "runs_allowed": 0
            }
        if away_team_id not in team_records:
            team_records[away_team_id] = {
            "name": away_team_name,
            "conference": "",
            "division": "",
            "wins": 0,
            "losses": 0,
            "runs_scored": 0,
            "runs_allowed": 0
            }
        home_score = game[7]
        away_score = game[8]
        home_win = game[9]
        team_records[home_team_id]["runs_scored"]+=home_score
        team_records[home_team_id]["runs_allowed"]+=away_score
        team_records[away_team_id]["runs_scored"]+=away_score
        team_records[away_team_id]["runs_allowed"]+=home_score
        if home_win == 1:
            team_records[home_team_id]["wins"]+=1
            team_records[away_team_id]["losses"]+=1
        else:
            team_records[away_team_id]["wins"]+=1
            team_records[home_team_id]["losses"]+=1
    
if __name__ == "__main__":
    year = 2016
    mydb = mysql.connector.connect(host = "127.0.0.1", 
                                user = "user", 
                                passwd="password1!")
    cursor = mydb.cursor()
    cursor.execute("USE MLB_GAMES;")
    cursor.execute("""
    CREATE TABLE mlb_standings (
    season INT,
    team VARCHAR(255),
    team_ID INT,
    wins INT,
    losses INT,
    runs_scored INT,
    runs_allowed INT,
    division  VARCHAR(255),
    conference VARCHAR(255)
    )
    """)
    while year < 2026:#save the standings from previous seasons
        calculateStandings(year)
        for team_ID, stats in team_records.items():
            name = stats["name"]
            wins = stats["wins"]
            losses = stats["losses"]
            runs_scored = stats["runs_scored"]
            runs_allowed = stats["runs_allowed"]
            cursor.execute("""
            SELECT *
            FROM mlb_teams
            WHERE team_ID = %s
            """, (team_ID,))
            result = cursor.fetchone()
            division = result[2]
            conference = result[3]
            cursor.execute("""
                INSERT INTO mlb_standings ( season, team, team_ID, wins, losses, 
                runs_scored, runs_allowed, division, conference)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (year, name, team_ID, wins, losses, runs_scored, runs_allowed,division, conference))

        team_records = {}
        year+=1
    mydb.commit()
    cursor.close()
    mydb.close()
