import sys
import boxscores
import potential
import standings
from awards import Awards

n = len(sys.argv)

if(n < 3):
	sys.exit("ERROR!  Must pass in year and week")

print("\nWELCOME TO THE LEAGUE!")

year = int(sys.argv[1])
week = int(sys.argv[2])

boxscores.calculate(year, week)
potential.calculate(year, week)
standings.calculate(year, week)

awards = Awards()
awards.calculate(year, week)
awards.update_awards(week)

print("\nUPDATE COMPLETE!")
