import smtplib

file = open("Stat Boy Information.txt", "r")
gmail_password = file.read()

sender_email = "fantasyfootballstatsboy@gmail.com"
receiver_email = "djransom90@gmail.com"

to = [receiver_email]
subject = "Testing 1"
body = "This is a test email.  It was sent from a python script on my desktop."
email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender_email, ", ".join(to), subject, body)

try:
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(sender_email, gmail_password)
	server.sendmail(sender_email, to, email_text)
	server.close()

	print('Email Sent!')
except Exception as e: print(e)