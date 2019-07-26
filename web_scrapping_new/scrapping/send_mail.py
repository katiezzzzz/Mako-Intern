import smtplib
from email.mime.text import MIMEText
import warnings

IP = '10.144.10.13'
port = 25

class SendEmail:

    def __init__(self):
        pass

    def send(self, to, message):
        msg = MIMEText(message, 'html')
        msg['From'] = 'DivAlert@mako.com'
        msg['To'] = to
        msg['Subject'] = 'Dividend Alerts'

        try:
            s = smtplib.SMTP(IP, port)
            s.send_message(msg)
        except:
            warnings.warn('Please update your IP address and port in send_mail.py')

if __name__ == "__main__":

    s = SendEmail()
    s.send('Katie.Zeng@mako.com,Jane.Jiang@mako.com', 'Hello, it works!!')