import sys
from stats import *

n = len(sys.argv)

if(n < 3):
	print("ERROR!  Must pass in year and week")

ff_stats = Stats(1525510, argv[1])

scores = ff_stats.get_boxscores(argv[2])
scores = list(scores)



