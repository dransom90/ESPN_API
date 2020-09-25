import sys
from stats import *

n = len(sys.argv)

if(n < 3):
	print("ERROR!  Must pass in year and week")

year = int(sys.argv[1])
week = int(sys.argv[2])

ff_stats = Stats(1525510, year)
potential = ff_stats.get_team_potential('LA Broncos', 2)
print(potential)