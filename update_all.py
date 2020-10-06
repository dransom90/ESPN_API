import sys
import boxscores
import potential
import standings
from stats import Stats
from awards import Awards

n = len(sys.argv)

if(n < 3):
	sys.exit("ERROR!  Must pass in year and week")

print("\nWELCOME TO THE LEAGUE!")

year = int(sys.argv[1])
week = int(sys.argv[2])

ff_stats = Stats(1525510, year)

boxscores.calculate(year, week, ff_stats)
potential.calculate(year, week, ff_stats)
standings.calculate(year, week, ff_stats)

awards = Awards(ff_stats)
awards.calculate(year, week)

print("\nUPDATE COMPLETE!")
