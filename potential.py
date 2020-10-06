import sys
from stats import *

def calculate(arg1, arg2):
	year = int(arg1)
	week = int(arg2)

	print("\nPOTENTIAL SCORE CALCULATOR")

	print("\nRetrieving Week " + str(week) + " data from ESPN")
	ff_stats = Stats(1525510, year)

	teams = ff_stats.get_teams()

	for x in teams:
		print("\n" + x.team_name)

		print("\tCalculating...")
		potential = ff_stats.get_team_potential(x, week)

		print("\tUpdating...")
		ff_stats.update_team_potential(x, potential, week)

if __name__ == "__calculate__":
	calculate(sys.argv[1], sys.argv[2])