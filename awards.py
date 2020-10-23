from stats import Stats
import pickle
import os
from apiclient import discovery
import httplib2
from google.oauth2 import service_account
from math import isclose

class Awards:
	def __init__(self, statistics: Stats):
		self.potential_scores = []
		self.game_scores = []
		self.high_scorer = ("None", -10)
		self.low_scorer = ("None", 1000)
		self.best_manager = ("None", 1000)
		self.worst_manager = ("None", -10)
		self.largest_victory = ("None", -1)
		self.smallest_victory = ("None", 1000)
		self.highest_potential = ("None", -10)
		self.lowest_potential = ("None", 1000)

		self.scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
		self.secret_file = "C:\\Users\\drans\\source\\repos\\CML The League Statistics\\client-secret.json"
		self.credentials = service_account.Credentials.from_service_account_file(self.secret_file, scopes=self.scopes)
		self.service = discovery.build('sheets', 'v4', credentials=self.credentials)
		self.SPREADSHEET_ID = '1tcIT9inKN5aElpOscdC9YDe6UKiP_kJWmJNX_TuEy7g'

		self.ff_stats = statistics

	def calculate(self, year: int, week: int):
		scores = self.ff_stats.get_boxscores(week)
		teams = self.ff_stats.get_teams()

		matchups = list(scores)

		print("\nAWARDS UPDATE")
		print("\n\tCalculating Awards From Box Scores")

		for match in matchups:
			home_name = match[0]
			home_score = match[1]
			away_name = match[2]
			away_score = match[3]

			home_team = get_team_from_name(home_name, teams)
			away_team = get_team_from_name(away_name, teams)

			self.add_score(home_name, home_score)
			self.add_score(away_name, away_score)

			potential = self.ff_stats.get_team_potential(home_team, week)
			self.add_potential_score(home_name, potential)

			potential = self.ff_stats.get_team_potential(away_team, week)
			self.add_potential_score(away_name, potential)

			if home_score > away_score:
				self.add_victory(home_name, home_score - away_score)
			if away_score > home_score:
				self.add_victory(away_name, away_score - home_score)

		print("\n\tCalculating Best and Worst Managers")
		self.worst_manager = self.get_worst_manager()
		self.best_manager = self.get_best_manager()
		self.update_awards(week)

	def add_score(self, team: str, score: float):
		self.game_scores.append((team, score))

		if score > self.high_scorer[1]:
			self.high_scorer = (team, score)
		elif score == self.high_scorer[1] and team != self.high_scorer[0]:
			self.high_scorer = (self.high_scorer[0] + ", " + team, score)
			
		if score < self.low_scorer[1]:
			self.low_scorer = (team, score)
		elif score == self.low_scorer[1]:
			self.low_scorer = (self.low_scorer[0] + ", " + team, score)

	def add_potential_score(self, team: str, score: float):
		self.potential_scores.append((team, score))

		if self.highest_potential[1] < score:
			self.highest_potential = (team, score)
		elif self.highest_potential[1] == score and team != self.highest_potential[0]:
			self.highest_potential = (self.highest_potential[0] + ", " + team, score)
			
		if self.lowest_potential[1] > score:
			self.lowest_potential = (team, score)
		elif self.lowest_potential[1] == score and team != self.lowest_potential:
			self.lowest_potential = (self.lowest_potential[0] + ", " + team, score)

	def add_victory(self, team: str, margin: float):
		if self.largest_victory[1] < margin:
			self.largest_victory = (team, margin)
		elif self.largest_victory[1] == margin and self.largest_victory[0] != team:
			self.largest_victory = (self.largest_victory[0] + ", " + team, margin)

		if self.smallest_victory[1] > margin:
			self.smallest_victory = (team, margin)
		elif self.smallest_victory[1] == margin and self.smallest_victory[0] != team:
			self.smallest_victory = (self.smallest_victory[0] + ", " + team, margin)

	def get_best_manager(self):
		best_manager = ("None", 1000)

		for game_score in self.game_scores:
			for potential in self.potential_scores:
				if potential[0] == game_score[0]:
					margin = abs(potential[1] - game_score[1])
					if margin < best_manager[1]:
						best_manager = (game_score[0], margin)
					elif isclose(margin - best_manager[1], 0, abs_tol = 1e-09):
						best_manager = (best_manager[0] + ", " + game_score[0], margin)
					break

		return best_manager	

	def get_worst_manager(self):
		worst_manager = ("None", -1)

		for game_score in self.game_scores:
			for potential in self.potential_scores:
				if potential[0] == game_score[0]:
					margin = potential[1] - game_score[1]
					if margin > worst_manager[1]:
						worst_manager = (game_score[0], margin)
					elif margin == potential[1]:
						worst_manager = (worst_manager[0] + ", " + game_score[0], margin)

		return worst_manager	

	def update_awards(self, week: int):
		cell_number = str(week + 2)
		
		print("\n\tUpdating Awards In Spreadsheet")
		range_name = 'Awards!' + 'B' + cell_number + ":I" + cell_number
		values = [
            [self.low_scorer[0], self.high_scorer[0], self.best_manager[0], self.worst_manager[0], self.highest_potential[0], self.lowest_potential[0], self.largest_victory[0], self.smallest_victory[0]]
        ]
		data = {'values' : values}

		self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

def get_team_from_name(name, teams):
	for team in teams:
		if team.team_name == name:
			return team