import sys
import boxscores
import potential
import standings

n = len(sys.argv)

if(n < 3):
	sys.exit("ERROR!  Must pass in year and week")

print("\nWELCOME TO THE LEAGUE!")

year = int(sys.argv[1])
week = int(sys.argv[2])

boxscores.calculate(year, week)
potential.calculate(year, week)
standings.calculate(year, week)

print("\nUPDATE COMPLETE!")
