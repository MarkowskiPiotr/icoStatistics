import configparser
import os
import smtplib
from datetime import date
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration.ini'))

port = config['MAIL']['port']
sender = config['MAIL']['sender']
receiver = config['MAIL']['receiver']
user = config['MAIL']['user']
password = config['MAIL']['password']

todayDate = date.today()
calendarWeek = todayDate.isocalendar()[1]


def sendEmail(data):
    msg = MIMEText(data)
    msg['Subject'] = 'CW' + str(calendarWeek) + ' ' + str(todayDate) + ' tests statistics'
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP("smtp.gmail.com", port) as server:
        server.starttls()  # Secure the connection

        server.login(user, password)
        server.sendmail(sender, receiver, msg.as_string())
        print("mail successfully sent")
