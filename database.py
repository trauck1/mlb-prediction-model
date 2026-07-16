import mysql.connector
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import json

#creates the database and game table
def createDataBase():
    mydb = mysql.connector.connect(host = "127.0.0.1", 
                                user = "user", 
                                passwd="password1!")

    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE MLB_GAMES;")
    cursor.execute("USE MLB_GAMES;")
    cursor.execute("""
    CREATE TABLE mlb_games (
    gameID INT PRIMARY KEY,
    season INT,
    date DATE,
    home_team VARCHAR(255),
    home_team_id INT,
    away_team VARCHAR(255),
    away_team_id INT,
    home_score INT,
    away_score INT,
    home_win BOOLEAN,
    away_win BOOLEAN,
    gameType  VARCHAR(255),
    url VARCHAR(255)
    )
    """)
    
    mydb.commit()
    cursor.close()
    mydb.close()

#starts at 2016 and ends at 7-14-2026
def iterateThroughURLs():
    baseURL = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date="
    startDate = date(2016, 1, 1)
    endDate = date(2026, 7, 14)#allstar break
    delta = timedelta(days=1)

    while startDate <= endDate:
        dateString = startDate.strftime("%Y-%m-%d")
        url = baseURL + dateString
        addGames(url, dateString)
        startDate += delta
#connects to the database created and adds all the mlb games
def addGames(url, gameDate):
    mydb = mysql.connector.connect(host = "127.0.0.1", 
                                user = "user", 
                                passwd="password1!")
    cursor = mydb.cursor()
    cursor.execute("USE MLB_GAMES;")
    #gets the json data from the source
    response = requests.get(url)
    data = response.json()
    
    for date in data["dates"]:
        for game in date["games"]:
            season = game["season"]
            #unique primary key
            gameID = game["gamePk"]
            gameType = game["seriesDescription"]
            officialDate = game["officialDate"]
            #if game gets canceled or rescheduled, the score and winner is set to None
            awayData = game["teams"]["away"]
            awayTeamID = awayData["team"]["id"]
            awayTeamName = awayData["team"]["name"]
            awayScore = awayData.get("score", None)
            awayWin = awayData.get("isWinner",None)
            
            homeData = game["teams"]["home"]
            homeTeamID = homeData["team"]["id"]
            homeTeamName = homeData["team"]["name"]
            homeScore = homeData.get("score", None)
            homeWin = homeData.get("isWinner",None)
            
            #if the game was started, but had to be finished on another date, skip and add on the other date
            if officialDate != gameDate:
                continue
            
            print(gameDate, gameID)
            #doesnt add any games that were canceled or postponed
            if homeScore != None and awayScore != None and homeWin != None and awayWin != None:
                cursor.execute("""
                    INSERT INTO mlb_games (gameID, season, date, home_team, home_team_id, away_team, 
                           away_team_id, home_score, away_score, home_win, away_win, gameType, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (gameID, season, officialDate, homeTeamName, homeTeamID, awayTeamName, awayTeamID, homeScore, 
                      awayScore, homeWin, awayWin, gameType, url))
    
    mydb.commit()
    cursor.close()
    mydb.close()




if __name__ == "__main__":
    #only call once, creates the database and adds every mlb game from the past 10 seasons
    #up to the allstar game of 2026
    createDataBase()
    iterateThroughURLs()
