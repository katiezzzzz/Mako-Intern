import smtplib
from email.mime.text import MIMEText

class SendEmail:

    def __init__(self):
        pass

    def send(self, to, message):
        msg = MIMEText(message, 'html')
        msg['From'] = 'DivAlert@mako.com'
        msg['To'] = to
        msg['Subject'] = 'Dividend Alerts'

        s = smtplib.SMTP('10.144.10.13', 25)
        s.send_message(msg)

if __name__ == "__main__":

    s = SendEmail()
    s.send('Katie.Zeng@mako.com,Jane.Jiang@mako.com', 'Hello, it works!!')