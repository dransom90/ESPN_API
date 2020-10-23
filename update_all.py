import sys
import boxscores
import potential
import standings
from stats import Stats
from awards import Awards
from email_update import EmailUpdate

n = len(sys.argv)

if(n < 3):
	sys.exit("ERROR!  Must pass in year and week")

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

ff_stats.update_season_record(week)
email_update.send_update()

print("\nUPDATE COMPLETE!")
