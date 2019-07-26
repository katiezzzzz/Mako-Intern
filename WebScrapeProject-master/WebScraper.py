'''
create a class with the following functions:
1. initializeCache - extract existing cache files or write new cache file
2. generateCache - generate info inside the class
3. compare - compare the updated website to original text file
4. alert - search for keywords in the compared file and send alerts
then update every 5 min
'''

import os.path
import csv
import warnings

from ScraperClasses.SendEmail import SendEmail
from ScraperClasses.RepeatEvery import RepeatEvery
from ScraperClasses.WebClass import WebClass

EmailList = 'katie.zeng@mako.com, jane.jiang@mako.com'

Frequency = 300
# frequency is in seconds

def update():
    if os.path.exists('Directory.csv'):
        message = []
        with open('Directory.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                company = str(row[0])
                URL = str(row[1])
                page = str(row[2])
                keywords = row[3].split(",")
                scrap = WebClass(URL, keywords, company, page)
                scrap.initializeCache()
                scrap.generateCache()
                scrap.compare()
                scrap.alert()
                if URL == None or keywords == None or company == None:
                    warnings.warn("Please check your directory. Missing entries found.")
                if scrap.createMessage() == None:
                    pass
                else:
                    message.append(scrap.createMessage())
                    if message != []:
                        message.append('<br>'+'\r\n'+'<br>')
            if message == []:
                pass
            else:
                message = ''.join(message)
                mail = SendEmail()
                mail.send(EmailList,message)
    else:
        warnings.warn("Please upload directory")
        exit()

if __name__ == "__main__":
    # run timer
    thread = RepeatEvery(Frequency, update)
    print("starting")
    thread.start()