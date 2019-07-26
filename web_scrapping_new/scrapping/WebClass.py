from bs4 import BeautifulSoup
import requests
import os.path
import pickle

my_path = "C:/Users/kzeng/PycharmProjects/python_training/web_scrapping_new/cache/"

class WebClass:

    def __init__(self, URL, keywords, company, page):
        #cache companypage is unique for each website
        self.company = company
        self.companypage = (company + " " + page)
        self.URL = URL
        self.keywords = keywords

    def initializeCache(self):
        # extract text from the website and convert all to lower case
        if os.path.exists(my_path + str(self.companypage) + '.p'):
            self.cache = pickle.load(open((my_path + str(self.companypage) + '.p'), 'rb'))
        else:
            soup = BeautifulSoup(requests.get(self.URL).text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            self.cache = soup.get_text().lower()
            self.cache = self.cache.replace('\n\n', ' ')
            self.cache = self.cache.split('\n')
            with open ((my_path + str(self.companypage) + '.p'),'wb') as f:
                pickle.dump(self.cache,f)

    def generateCache(self):
        self.old_line = []
        for line in self.cache:
            for word in self.keywords:
                if word in line:
                    self.old_line.append(line)

    def compare(self):
        self.new_line = []
        # compare the previous website to updated version
        newsoup = BeautifulSoup(requests.get(self.URL).text, "html.parser")
        for script in newsoup(["script", "style"]):
            script.decompose()
        new = newsoup.get_text().lower()
        new = new.replace('\n\n', ' ')
        new = new.split('\n')
        if new == self.cache:
            print("No new updates at " + self.companypage)
        else:
            print("New updates at " + self.companypage)
            for line in new:
                for word in self.keywords:
                    if word in line:
                        self.new_line.append(line)
        self.cache = new
        with open((my_path + str(self.companypage) + '.p'), 'wb') as f:
            pickle.dump(self.cache, f)

    def alert(self):
        self.new_line.reverse()
        for line in self.old_line:
            if line in self.new_line:
                self.new_line.remove(line)
        if self.new_line:
            self.new_line.reverse()
            self.message = ["New updates at " + self.companypage + ':' + '\r\n' + self.URL + '\r\n']
            print(self.URL)
            for line in self.new_line:
                print(line)
                self.message.append(line + '\r\n')

    def createMessage(self):
        if self.new_line:
            return ''.join(self.message)