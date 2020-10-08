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

class Stats:
	"""Retrieves information from ESPN.  Calculates statistics and updates the spreadsheet"""
	def __init__(self, league_id: int, year: int):
		self.league = League(league_id=league_id, year=year)

		self.scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
		self.secret_file = "C:\\Users\\drans\\source\\repos\\CML The League Statistics\\client-secret.json"
		self.credentials = service_account.Credentials.from_service_account_file(self.secret_file, scopes=self.scopes)
		self.service = discovery.build('sheets', 'v4', credentials=self.credentials)
		self.SPREADSHEET_ID = '1tcIT9inKN5aElpOscdC9YDe6UKiP_kJWmJNX_TuEy7g'

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
			"mike dopp" : "C8",
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
			"mike dopp" : "F8",
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
			"mike dopp" : "D8",
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
			"mike dopp" : "W40",
			"KJ Patterson" : "W41",
			"Jestin Vanderloo" : "W42",
			"Bradley Leyland" : "W43",
			"DJ Ransom" : "W44",
		}

	def get_luck_information(self, week: int):
		"""Retrieves the luck scores from the spreadsheet and returns a list of tuples
		(Team Owner, W/L, beat/lost to, # of teams, Luck Score)
		Update the spreadsheet before calling this function."""

		print("Retrieving spreadsheets")
		luck = self.spreadsheet.worksheet("Luck")
		week_page = self.spreadsheet.worksheet("Week " + str(week))
		
		print("Retrieving scores")
		week_scores = week_page.batch_get(['C3:C12'])
		scores = []
		for x in week_scores[0]:
			scores.append(float(x[0]))

		print("Retrieving win/loss")
		win_loss = week_page.batch_get(['H3:H12'])
		results = []
		for x in win_loss[0]:
			results.append(str(x[0]))

		with open('Owners.txt') as f:
			owners = f.read().splitlines()

		print("Retrieving luck scores")
		row_number = week + 1
		range = 'B' + str(row_number) + ':K' + str(row_number)
		week_luck = luck.batch_get([range])

		luck_report = []

		print("Compiling Luck Report")
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
			yield (scores.home_team.team_name, scores.home_score, scores.away_team.team_name, scores.away_score)

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

		for x in range(5):
			if str(box_scores[x].home_team.team_name) == team.team_name:
				lineup = box_scores[x].home_lineup
				break
			elif str(box_scores[x].away_team.team_name) == team.team_name:
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