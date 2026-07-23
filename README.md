# mlb-prediction-model (IN PROGRESS)


## Overview

This project is a machine learning pipeline for predicting the rest of the 2026 MLB Season. The current focus is on building a historical database and generating team statistics from the last 10 years that will later be used to train a predictive model.

The project uses the MLB Stats API to collect historical game data, stores it in a MySQL database, and computes season standings.

The long-term goal is to use these features to predict the outcome of the remaining games in the current MLB season.

---

## Current Progress

### Historical Game Database (database.py)

* Downloaded every MLB game from the 2016 season through the 2026 All-Star Break using the MLB Stats API.
* Stored all completed games in a MySQL database.
* Automatically skips postponed, cancelled, and suspended games to avoid duplicate game IDs.
* Updates historical team names ( Cleveland Indians → Cleveland Guardians) for consistency.
* Creates a second table containing the remaining scheduled games for the 2026 season that will eventually be used for predictions.

---

###  Team Database (teamsTable.py)

The project creates a separate `mlb_teams` table containing:

* Team ID
* Team Name
* League (American / National)
* Division

This information is pulled directly from the MLB Stats API and is used when generating season standings.

---

###  Season Standings Generator (standings.py)

A standings generator iterates through every day of a season and updates each team's statistics as games are played.

Currently tracked statistics include:

* Wins
* Losses
* Runs Scored
* Runs Allowed

At the end of each season (2016–2025), the final standings are saved into a MySQL standings table.


---

## Database Structure

### `mlb_games`

Stores every completed MLB game.

| Column       |
| ------------ |
| gameID       |
| season       |
| date         |
| home_team    |
| home_team_id |
| away_team    |
| away_team_id |
| home_score   |
| away_score   |
| home_win     |
| away_win     |
| gameType     |
| url          |

---

### `mlb_schedule`

Stores future scheduled games for the remainder of the 2026 season.

---

### `mlb_teams`

Stores team information.

| Column     |
| ---------- |
| team_ID    |
| team_name  |
| division   |
| conference |

---

### `mlb_standings`

Stores each team's final season statistics.

| Column       |
| ------------ |
| season       |
| team         |
| team_ID      |
| wins         |
| losses       |
| runs_scored  |
| runs_allowed |
| division     |
| conference   |

---

## Project Structure

```text
mlb-prediction-model/
│
├── database.py
│   Creates the database, downloads historical games,
│   saves future scheduled games, and cleans historical data.
│
├── teamstable.py
│   Downloads all MLB teams and creates the team lookup table.
│
└── standings.py
    Replays each season game-by-game and generates season standings
    from the historical database.
```

---

## Technologies

* Python
* MySQL
* MLB Stats API
* Requests

---


---


