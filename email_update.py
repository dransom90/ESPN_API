import smtplib, ssl
import getpass

sender_email = "fantasyfootballstatsboy@gmail.com"
receiver_email = "djransom90@gmail.com"
port = 465
password = getpass.getpass(prompt='Password: ', stream=None)

context = ssl.create_default_context()

message = """\
Subject: Testing

This is a test email.  It was sent from a python script on my desktop."""

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)