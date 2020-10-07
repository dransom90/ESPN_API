import sys
from stats import *

def calculate(arg1, arg2, arg3):
	year = int(arg1)
	week = int(arg2)
	ff_stats = arg3

	print("\nPOTENTIAL SCORE CALCULATOR")

	print("\nRetrieving Week " + str(week) + " data from ESPN")

	teams = ff_stats.get_teams()

	for x in teams:
		print("\n" + x.team_name)

		print("\tCalculating...")
		potential = ff_stats.get_team_potential(x, week)

		print("\tUpdating...")
		ff_stats.update_team_potential(x, potential, week)

if __name__ == "__calculate__":
	calculate(sys.argv[1], sys.argv[2], sys.argv[3])