import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from stats import Stats
from awards import Awards

class EmailUpdate:
	def __init__(self, statistics: Stats, awards: Awards, week: int):
		self.ff_stats = statistics
		self.awards = awards
		self.week = week
		self.plain_text = ""
		self.html = ""

	def send_update(self):
		print("\nEMAIL UPDATE")
		self.create_email_body()
		self.send_email()

	def create_email_body(self):
		print("\tCompiling email body")
		
		self.compile_awards_summary()
		self.compile_luck_summary()

	def compile_awards_summary(self):
		print("\t\tCompiling Awards Summary")
		high_score = self.awards.high_scorer
		low_score = self.awards.low_scorer
		high_potential = self.awards.highest_potential
		low_potential = self.awards.lowest_potential
		largest_victory = self.awards.largest_victory
		smallest_victory = self.awards.smallest_victory
		
		self.plain_text += '\n'
		self.plain_text += ('\n' + high_score[0] + " is the top scorer with " + str(high_score[1]) + " points")
		self.plain_text += ('\n' + low_score[0] + " is the low scorer with " + str(low_score[1]) + " points")
		self.plain_text += ('\n' + high_potential[0] + " had the highest potential with " + str(high_potential[1]) + " points")
		self.plain_text += ('\n' + low_potential[0] + " had the lowest potential with " + str(low_potential[1]) + " points")
		self.plain_text += ('\n' + largest_victory[0] + " had the largest victory with " + str(largest_victory[1]) + " points")
		self.plain_text += ('\n' + smallest_victory[0] + " had the smallest victory with " + str(smallest_victory[1]) + " points")
		self.plain_text += '\n'

	def compile_luck_summary(self):
		print("\t\tCompiling Luck Summary")
		self.plain_text += '\n'
		#TODO:  Figure out HTML
		luck_information = self.ff_stats.get_luck_information(self.week)
		i = 0
		for x in luck_information:
			if luck_information[i][1] == 'W':
				win_loss = 'won'
			else:
				win_loss = 'lost'

			next_line = str(luck_information[i][0]) + ' ' + win_loss + ' and would have ' + str(luck_information[i][2]) + ' ' + str(luck_information[i][3]) + ' teams.  Luck Score: ' + str(luck_information[i][4])
			self.plain_text += ('\n' + next_line)
			i += 1
		self.plain_text += '\n'

	def send_email(self):
		print("\tLogging into email")
		file = open("Stat Boy Information.txt", "r")
		gmail_password = file.read()
		subject = "Week " + str(self.week) + " Report"

		sender_email = "fantasyfootballstatsboy@gmail.com"
		receiver_email = "djransom90@gmail.com"

		print("\tCompiling email")
		message= MIMEMultipart("alternative")
		message["Subject"] = subject
		message["From"] = sender_email
		message["To"] = receiver_email

		plain_text = MIMEText(self.plain_text, "plain")
		message.attach(plain_text)

		print("\tSending email")
		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(sender_email, gmail_password)
			server.sendmail(sender_email, receiver_email, message.as_string())
			server.close()

			print('\tEmail Sent!')
		except Exception as e: print(e)