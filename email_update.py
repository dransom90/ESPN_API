import smtplib
from stats import Stats
from awards import Awards

class EmailUpdate:
	def __init__(self, statistics: Stats, awards: Awards, week: int):
		self.ff_stats = statistics
		self.awards = awards
		self.body = ""
		self.week = week

	def create_email_body(self):
		print("Compiling email body")
		luck_information = self.ff_stats.get_luck_information(self.week)

		i = 0
		for x in luck_information:
			if luck_information[i][1] == 'W':
				win_loss = 'won'
			else:
				win_loss = 'lost'

			next_line = str(luck_information[i][0]) + ' ' + win_loss + ' and would have ' + str(luck_information[i][2]) + ' ' + str(luck_information[i][3]) + ' teams.  Luck Score: ' + str(luck_information[i][4])
			self.body += ('\n' + next_line)
			i += 1

	def send_email(self):
		print("Logging into email")
		file = open("Stat Boy Information.txt", "r")
		gmail_password = file.read()

		sender_email = "fantasyfootballstatsboy@gmail.com"
		receiver_email = "djransom90@gmail.com"

		print("Compiling email")
		to = [receiver_email]
		subject = "Week " + str(self.week) + " Report"
		body = self.body
		email_text = """\
		From: %s
		To: %s
		Subject: %s

		%s
		""" % (sender_email, ", ".join(to), subject, body)

		print("Sending email")
		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(sender_email, gmail_password)
			server.sendmail(sender_email, to, email_text)
			server.close()

			print('Email Sent!')
		except Exception as e: print(e)