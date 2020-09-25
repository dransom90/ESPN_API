from ESPN_API.football import *
import pickle
import os
from apiclient import discovery
import httplib2
from google.oauth2 import service_account
from py_linq import Enumerable

class Stats:
    def __init__(self, league_id: int, year: int):
        self.league = League(league_id=league_id, year=year)

        self.scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        self.secret_file = "C:\\Users\drans\\source\\repos\\CML The League Statistics\\client_secret.json"
        self.credentials = service_account.Credentials.from_service_account_file(self.secret_file, scopes=self.scopes)
        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)
        self.SPREADSHEET_ID = '1tcIT9inKN5aElpOscdC9YDe6UKiP_kJWmJNX_TuEy7g'

        # Team Name to Spreadsheet Cell Dictionary
        # Points Scored
        self.name_to_cell = {
	        "Hey Baby Let's Go to Vegas" : "C3",
	        "LA Broncos" : "C4",
	        "The Chizwit" : "C5",
	        "how 'bout them Cowboys" : "C6",
	        "Dos Equis" : "C7",
	        "cant stop the dopp" : "C8",
	        "Cobra Kai" : "C9",
	        "pirate  angel" : "C10",
	        "Snickle Fritz" : "C11",
	        "Discount  Belichick" : "C12",
	    }

        # Team Name to Spreadsheet Cell Dictionary
        # PA
        self.name_to_points_against_cell = {
	        "Hey Baby Let's Go to Vegas" : "F3",
	        "LA Broncos" : "F4",
	        "The Chizwit" : "F5",
	        "how 'bout them Cowboys" : "F6",
	        "Dos Equis" : "F7",
	        "cant stop the dopp" : "F8",
	        "Cobra Kai" : "F9",
	        "pirate  angel" : "F10",
	        "Snickle Fritz" : "F11",
	        "Discount  Belichick" : "F12",
	    }

        # Team Name to Spreadsheet Cell Dictionary
        # PA
        self.name_to_potential_cell = {
	        "Hey Baby Let's Go to Vegas" : "D3",
	        "LA Broncos" : "D4",
	        "The Chizwit" : "D5",
	        "how 'bout them Cowboys" : "D6",
	        "Dos Equis" : "D7",
	        "cant stop the dopp" : "D8",
	        "Cobra Kai" : "D9",
	        "pirate  angel" : "D10",
	        "Snickle Fritz" : "D11",
	        "Discount  Belichick" : "D12",
	    }

        # Team Name to Spreadsheet Cell Dictionary
        # Standings
        self.name_to_standings_cell = {
	        "Hey Baby Let's Go to Vegas" : "W35",
	        "LA Broncos" : "W36",
	        "The Chizwit" : "W37",
	        "how 'bout them Cowboys" : "W38",
	        "Dos Equis" : "W39",
	        "cant stop the dopp" : "W40",
	        "Cobra Kai" : "W41",
	        "pirate  angel" : "W42",
	        "Snickle Fritz" : "W43",
	        "Discount  Belichick" : "W44",
	    }

    def get_boxscores(self, week: int):
        box_scores = self.league.box_scores(week)

        for scores in box_scores:
            yield (scores.home_team.team_name, scores.home_score, scores.away_team.team_name, scores.away_score)

    def update_team_boxscore(self, team: str, score: float, week: int):
        
        range_name = 'Week ' + str(week) + '!' + self.name_to_cell[team]
        values = [
            [score]
        ]
        data = {'values' : values}

        self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

    def update_team_points_against(self, team: str, score: float, week: int):

        range_name = 'Week ' + str(week) + '!' + self.name_to_points_against_cell[team]
        values = [
            [score]
        ]
        data = {'values' : values}

        self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()
    
    def get_team_potential(self, team: str, week: int):
        box_scores = self.league.box_scores(week)
        lineup = None

        for x in range(5):
            if str(box_scores[x].home_team.team_name) == team:
                lineup = box_scores[x].home_lineup
                break
            elif str(box_scores[x].away_team.team_name) == team:
                lineup = box_scores[x].away_lineup
                break
        
        n = len(lineup)

        potential = 0.0
        qb_scores = []
        rb_scores = []
        wr_scores = []
        te_scores = []
        dp_scores = []
        hc_scores = []
        flex_scores = []

        dp_positions = ['LB', 'S', 'DE', 'EDR', 'DT', 'CB']

        for x in range(n):
            pos = lineup[x].position
            score = lineup[x].points

            if pos == "TQB":
                qb_scores.append(score)
            elif pos == "RB":
                rb_scores.append(score)
            elif pos == "WR":
                wr_scores.append(score)
            elif pos == "TE":
                te_scores.append(score)
            elif pos in dp_positions:
                dp_scores.append(score)
            elif pos == "HC":
                hc_scores.append(score)

        potential += max(qb_scores)
        potential += max(rb_scores)

        rb_scores.remove(max(rb_scores))
        potential += max(rb_scores)
        rb_scores.remove(max(rb_scores))

        potential += max(wr_scores)
        wr_scores.remove(max(wr_scores))
        potential += max(wr_scores)
        wr_scores.remove(max(wr_scores))

        potential += max(te_scores)
        te_scores.remove(max(te_scores))

        if rb_scores:
            flex_scores.append(max(rb_scores))
        if wr_scores:
            flex_scores.append(max(wr_scores))
        if te_scores:
            flex_scores.append(max(te_scores))

        potential += max(flex_scores)

        if dp_scores:
            potential += max(dp_scores)
        if hc_scores:
            potential += max(hc_scores)
        
        return potential

    def update_team_potential(self, team: str, score: float, week: int):
        range_name = 'Week ' + str(week) + '!' + self.name_to_potential_cell[team]
        values = [
            [score]
        ]
        data = {'values' : values}

        self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

    def update_standings(self, week: int):
        standings = self.league.standings()

        n = len(standings)

        for x in range(n):
            name = standings[x].team_name
            pos = x + 1
            range_name = 'Team Performance' + '!' + self.name_to_standings_cell[name]
            values = [
                [pos]
            ]
            data = {'values' : values}
            self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()