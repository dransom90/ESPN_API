import sys
from stats import *

n = len(sys.argv)

if(n < 3):
	print("ERROR!  Must pass in year and week")

print("POTENTIAL SCORE CALCULATOR")

year = int(sys.argv[1])
week = int(sys.argv[2])

print("Retrieving data from ESPN")
ff_stats = Stats(1525510, year)

teams = ["Hey Baby Let's Go to Vegas", "LA Broncos", "The Chizwit", "how 'bout them Cowboys", "Dos Equis", "cant stop the dopp", "Cobra Kai", "pirate  angel", "Snickle Fritz", "Discount  Belichick"]

for x in teams:
	print(x)

	print("Calculating...")
	potential = ff_stats.get_team_potential(x, week)

	print("Updating...")
	ff_stats.update_team_potential(x, potential, week)