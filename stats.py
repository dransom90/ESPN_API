from ESPN_API.football import *
import pickle
import os
from apiclient import discovery
import httplib2
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from py_linq import Enumerable
import numpy as np
from decimal import *
import pandas as pd

class Stats:
	"""Retrieves information from ESPN.  Calculates statistics and updates the spreadsheet"""
	def __init__(self, league_id: int, year: int):
		self.league = League(league_id=league_id, year=year)

		self.scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
		self.secret_file = "C:\\Users\\drans\\source\\repos\\CML The League Statistics\\client-secret.json"
		self.credentials = service_account.Credentials.from_service_account_file(self.secret_file, scopes=self.scopes)
		self.service = discovery.build('sheets', 'v4', credentials=self.credentials)
		self.SPREADSHEET_ID = '1g5Q538yWN_fCTbepA17ckjIqAErp3tDeBJaF0okJCZk'

		self.client = gspread.authorize(self.credentials)
		self.spreadsheet = self.client.open_by_key(self.SPREADSHEET_ID)

		# Team Name to Spreadsheet Cell Dictionary
		# Points Scored
		self.name_to_cell = {
			"Ryan Muranaka" : "C3",
			"Chad Spring" : "C4",
			"Mark Andrews" : "C5",
			"David Lopez" : "C6",
			"Caya Muranaka" : "C7",
			"Kyle Tensmeyer" : "C8",
			"KJ Patterson" : "C9",
			"Jestin Vanderloo" : "C10",
			"Bradley Leyland" : "C11",
			"DJ Ransom" : "C12",
		}

		# Team Name to Spreadsheet Cell Dictionary
		# PA
		self.name_to_points_against_cell = {
			"Ryan Muranaka" : "F3",
			"Chad Spring" : "F4",
			"Mark Andrews" : "F5",
			"David Lopez" : "F6",
			"Caya Muranaka" : "F7",
			"Kyle Tensmeyer" : "F8",
			"KJ Patterson" : "F9",
			"Jestin Vanderloo" : "F10",
			"Bradley Leyland" : "F11",
			"DJ Ransom" : "F12",
		}

		# Team Name to Spreadsheet Cell Dictionary
		# PA
		self.name_to_potential_cell = {
			"Ryan Muranaka" : "D3",
			"Chad Spring" : "D4",
			"Mark Andrews" : "D5",
			"David Lopez" : "D6",
			"Caya Muranaka" : "D7",
			"Kyle Tensmeyer" : "D8",
			"KJ Patterson" : "D9",
			"Jestin Vanderloo" : "D10",
			"Bradley Leyland" : "D11",
			"DJ Ransom" : "D12",
		}

		# Team Name to Spreadsheet Cell Dictionary
		# Standings
		self.name_to_standings_cell = {
			"Ryan Muranaka" : "W35",
			"Chad Spring" : "W36",
			"Mark Andrews" : "W37",
			"David Lopez" : "W38",
			"Caya Muranaka" : "W39",
			"Kyle Tensmeyer" : "W40",
			"KJ Patterson" : "W41",
			"Jestin Vanderloo" : "W42",
			"Bradley Leyland" : "W43",
			"DJ Ransom" : "W44",
		}

	def update_team_names(self):
		"""Retrieves the Team Owners and current Team Names from ESPN and updates the spreadsheet accordingly"""

		print("\nTEAM NAME UPDATE")
		team_names = []

		with open('Owners to Cell.txt') as f:
			owner_info = f.read().splitlines()

		teams = self.league.teams

		for info in owner_info:
			split_info = info.split('-')
			name = split_info[0].strip()

			for team in teams:
				if name == team.owner:
					team_names.append(team.team_name)
					break

		team_page = self.spreadsheet.worksheet("Teams")
		cell_list = team_page.range('B2:B11')

		i = 0
		for cell in cell_list:
			cell.value = team_names[i]
			i += 1

		team_page.update_cells(cell_list)

	def determine_winning_streak(self):
		"""Calculates and updates the longest winning streak for each team"""
		result_page = self.spreadsheet.worksheet("Win/Loss")

		for i in range(0, 10):
			cell_range = 'B' + str(i + 2) + ':Q' + str(i + 2)
			results = result_page.batch_get([cell_range])

			flat_results = []
			for sublist in results:
				for entries in sublist:
					for entry in entries:
						if entry == 'W':
							flat_results.append(1)
						else:
							flat_results.append(0)

			df = pd.DataFrame({'W': flat_results})

			grouper = (df.W != df.W.shift()).cumsum()
			df['streak'] = df.groupby(grouper).cumsum()

			streak = max(df['streak'])
			result_page.batch_update([{
					'range': 'S' + str(i + 2),
					'values': [[streak]],
					}])

	def determine_losing_streak(self):
		"""Calculates and updates the longest losing streak for each team"""
		result_page = self.spreadsheet.worksheet("Win/Loss")

		for i in range(0, 10):
			cell_range = 'B' + str(i + 2) + ':Q' + str(i + 2)
			results = result_page.batch_get([cell_range])

			flat_results = []
			for sublist in results:
				for entries in sublist:
					for entry in entries:
						if entry == 'L':
							flat_results.append(1)
						else:
							flat_results.append(0)

			df = pd.DataFrame({'W': flat_results})

			grouper = (df.W != df.W.shift()).cumsum()
			df['streak'] = df.groupby(grouper).cumsum()

			streak = max(df['streak'])
			result_page.batch_update([{
					'range': 'T' + str(i + 2),
					'values': [[streak]],
					}])

	def update_season_record(self, week: int):
		"""Retrieves the all of the season scores and victory margins up to the designated week.  Updates the spreadsheets with the high and lows for each."""
		
		print("\nUpdating Season Records")
		score_page = self.spreadsheet.worksheet("Scores")
		scores = score_page.batch_get(['C4:C19', 'E4:E19', 'G4:G19', 'I4:I19', 'K4:K19', 'M4:M19', 'O4:O19', 'Q4:Q19', 'S4:S19', 'U4:U19'])

		flat_scores = []
		for sublist in scores:
			for item in sublist:
				flat_scores.append(float(item[0]))
		
		victory_margins = []

		for i in range(1, week + 1):
			week_page = self.spreadsheet.worksheet("Week " + str(i))
			victory_margins.append(week_page.batch_get(['G3:G12']))

		flat_victories = []
		for sublist in victory_margins:
			for item in sublist:
				for margin in item:
					if margin:
						flat_victories.append(float(margin[0]))

		high_score = max(flat_scores)
		low_score = min(flat_scores)
		largest_victory = max(flat_victories)
		smallest_victory = min(flat_victories)

		season_record_page = self.spreadsheet.worksheet("Season Records")
		season_record_page.batch_update([{
			'range': 'B2:E2',
			'values': [[high_score, low_score, largest_victory, smallest_victory]],
			}])

	def get_luck_information(self, week: int):
		"""Retrieves the luck scores from the spreadsheet and returns a list of tuples
		(Team Owner, W/L, beat/lost to, # of teams, Luck Score)
		Update the spreadsheet before calling this function."""

		luck = self.spreadsheet.worksheet("Luck")
		week_page = self.spreadsheet.worksheet("Week " + str(week))
		
		# Retrieving scores
		week_scores = week_page.batch_get(['C3:C12'])
		scores = []
		for x in week_scores[0]:
			scores.append(float(x[0]))

		# Retrieving win/loss from spreadsheet
		win_loss = week_page.batch_get(['H3:H12'])
		results = []
		for x in win_loss[0]:
			results.append(str(x[0]))

		with open('Owners.txt') as f:
			owners = f.read().splitlines()

		# Retrieving luck scores from spreadsheet
		row_number = week + 1
		range = 'B' + str(row_number) + ':K' + str(row_number)
		week_luck = luck.batch_get([range])

		luck_report = []

		# Compiling Luck Report
		i = 0
		for x in week_luck[0][0]:
			if results[i] == 'W':
				verb = 'lost to'
				teams = sum(x > scores[i] for x in scores)
			else:
				verb = 'beat'
				teams = sum(x < scores[i] for x in scores)

			luck_report.append((owners[i], results[i], verb, teams, x))
			i += 1

		return luck_report

	def get_teams(self):
		return self.league.teams

	def get_boxscores(self, week: int):
		box_scores = self.league.box_scores(week)

		for scores in box_scores:
			try:
				yield (scores.home_team.team_name, scores.home_score, scores.away_team.team_name, scores.away_score)
			except AttributeError:
				if scores.home_team == 0:
					yield ("BYE", 0, scores.away_team.team_name, scores.away_score)
				elif scores.away_team == 0:
					yield (scores.home_team.team_name, scores.home_score, "BYE", 0)

	def update_team_boxscore(self, team: Team, score: float, week: int):

		range_name = 'Week ' + str(week) + '!' + self.name_to_cell[team.owner]
		values = [[score]]
		data = {'values' : values}

		self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

	def update_team_points_against(self, team: Team, score: float, week: int):

		range_name = 'Week ' + str(week) + '!' + self.name_to_points_against_cell[team.owner]
		values = [[score]]
		data = {'values' : values}

		self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

	def get_team_potential(self, team: Team, week: int):
		box_scores = self.league.box_scores(week)
		lineup = None

		count = len(list(box_scores))

		for x in range(count):
			if str(box_scores[x].home_team.team_name) == team.team_name:
				lineup = box_scores[x].home_lineup
				break
			elif str(box_scores[x].away_team != 0 and box_scores[x].away_team.team_name) == team.team_name:
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
		k_scores = []
		dst_scores = []
		flex_scores = []

		dp_positions = ['LB', 'S', 'DE', 'EDR', 'DT', 'CB']

		for x in range(n):
			pos = lineup[x].position
			score = lineup[x].points

			if pos == "QB":
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
			elif pos == "K":
				k_scores.append(score)
			elif pos == "D/ST":
				dst_scores.append(score)

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
		if k_scores:
			potential += max(k_scores)
		if dst_scores:
			potential += max(dst_scores)

		return potential

	def update_team_potential(self, team: Team, score: float, week: int):
		range_name = 'Week ' + str(week) + '!' + self.name_to_potential_cell[team.owner]
		values = [[score]]
		data = {'values' : values}

		self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

	def update_standings(self, week: int):
		standings = self.league.standings()

		n = len(standings)

		for x in range(n):
			team = standings[x]
			pos = x + 1
			range_name = 'Team Performance' + '!' + self.name_to_standings_cell[team.owner]
			values = [[pos]]
			data = {'values' : values}
			self.service.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()