import sys
from stats import *

n = len(sys.argv)

if(n < 3):
	print("ERROR!  Must pass in year and week")

print("WELCOME TO THE LEAGUE!")

year = int(sys.argv[1])
week = int(sys.argv[2])

print("Retrieving data from ESPN")
ff_stats = Stats(1525510, year)

print("Retrieving Box Scores for Week" + str(week))
scores = ff_stats.get_boxscores(week)
matchups = list(scores)

for match in matchups:
	home_name = match[0]
	home_score = match[1]
	away_name = match[2]
	away_score = match[3]

	
	print("Updating " + str(home_name))
	print("Score: " + str(home_score) + " PA: " + str(away_score))
	ff_stats.update_team_boxscore(str(home_name), float(home_score), week)
	ff_stats.update_team_points_against(str(home_name), float(away_score), week)

	print("Updating " + str(away_name))
	print("Score: " + str(away_score) + " PA: " + str(home_score))
	ff_stats.update_team_boxscore(str(away_name), float(away_score), week)
	ff_stats.update_team_points_against(str(away_name), float(home_score), week)