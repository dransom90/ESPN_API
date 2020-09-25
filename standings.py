import sys
from stats import *

def calculate(arg1, arg2):
	year = int(arg1)
	week = int(arg2)

	print("\nSTANDINGS UPDATE")

	print("\nRetrieving data from ESPN")
	ff_stats = Stats(1525510, year)

	print("\nUpdating standings...")
	ff_stats.update_standings(3)

if __name__ == "__calculate__":
	calculate(sys.argv[1], sys.argv[2])
