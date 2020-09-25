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
        print("Not Implemented!")

    def update_team_potential(self, team: str, score: float, week: int):
        print("Not Implemented!")
