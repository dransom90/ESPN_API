import sys
from stats import *

def calculate(arg1, arg2, arg3):
	year = int(arg1)
	week = int(arg2)
	ff_stats = arg3

	print("\nSTANDINGS UPDATE")

	print("\nUpdating standings...")
	ff_stats.update_standings(3)

if __name__ == "__calculate__":
	calculate(sys.argv[1], sys.argv[2], sys.argv[3])
