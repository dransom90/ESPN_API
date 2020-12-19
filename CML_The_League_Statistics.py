# Use this code to help with debugging
import sys
import boxscores
import potential
import standings
#from time import clock
from stats import Stats
from awards import Awards
from email_update import EmailUpdate

n = len(sys.argv)

if(n < 3):
	sys.exit("ERROR!  Must pass in year and week")

#start_time = time.clock()
#print(start_time)

print("\nWELCOME TO THE LEAGUE!")

year = int(sys.argv[1])
week = int(sys.argv[2])

ff_stats = Stats(1525510, year)
awards = Awards(ff_stats)
email_update = EmailUpdate(ff_stats, awards, week)

boxscores.calculate(year, week, ff_stats)
potential.calculate(year, week, ff_stats)
standings.calculate(year, week, ff_stats)
awards.calculate(year, week)

ff_stats.update_team_names()
ff_stats.update_season_record(week)
ff_stats.determine_winning_streak()
ff_stats.determine_losing_streak()
email_update.send_update()

print("\nUPDATE COMPLETE!")