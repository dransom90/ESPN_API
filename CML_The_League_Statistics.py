from stats import Stats
from email_update import EmailUpdate
from awards import Awards

print("Initializing.  Stand by...")
ff_stats = Stats(1525510, 2020)
ff_awards = Awards(ff_stats)
email_update = EmailUpdate(ff_stats, ff_awards, 4)

email_update.create_email_body()
email_update.send_email()