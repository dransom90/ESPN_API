import sys
from stats import *

def calculate(arg1, arg2):
	year = int(arg1)
	week = int(arg2)

	print("\nBOX SCORES CALCULATOR")

	print("\nRetrieving data from ESPN")
	ff_stats = Stats(1525510, year)

	teams = ff_stats.get_teams()

	print("\nRetrieving Box Scores for Week" + str(week) + "\n")
	scores = ff_stats.get_boxscores(week)
	matchups = list(scores)

	for match in matchups:
		home_name = match[0]
		home_score = match[1]
		away_name = match[2]
		away_score = match[3]

		home_team = get_team_from_name(home_name, teams)
		away_team = get_team_from_name(away_name, teams)

		print("\tUpdating " + str(home_name))
		print("\t\tScore: " + str(home_score) + " PA: " + str(away_score))
		ff_stats.update_team_boxscore(home_team, float(home_score), week)
		ff_stats.update_team_points_against(home_team, float(away_score), week)

		print("\tUpdating " + str(away_name))
		print("\t\tScore: " + str(away_score) + " PA: " + str(home_score))
		ff_stats.update_team_boxscore(away_team, float(away_score), week)
		ff_stats.update_team_points_against(away_team, float(home_score), week)

def get_team_from_name(name, teams):
	for team in teams:
		if team.team_name == name:
			return team

if __name__ == "__calculate__":
	calculate(sys.argv[1], sys.argv[2])