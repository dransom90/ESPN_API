import sys
from stats import *

n = len(sys.argv)

if(n < 3):
	print("ERROR!  Must pass in year and week")

print("POTENTIAL SCORE CALCULATOR")

year = int(sys.argv[1])
week = int(sys.argv[2])

print("\nRetrieving data from ESPN")
ff_stats = Stats(1525510, year)

ff_stats.update_standings(3)
