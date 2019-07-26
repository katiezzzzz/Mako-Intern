from bs4 import BeautifulSoup
import requests
import os.path
import pickle
import urllib.request
import warnings

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
            try:
                requests.get(self.URL).raise_for_status()
                soup = BeautifulSoup(requests.get(self.URL).text, 'html.parser')
                print(urllib.request.urlopen(self.URL).getcode())
                for script in soup(["script", "style"]):
                    script.decompose()
                self.cache = soup.get_text().lower()
                self.cache = self.cache.replace('\n\n', ' ')
                self.cache = self.cache.split('\n')
                with open ((my_path + str(self.companypage) + '.p'),'wb') as f:
                    pickle.dump(self.cache,f)
            except:
                warnings.warn(self.companypage + ' webpage down')
                self.cache = []

    def generateCache(self):
        self.old_line = []
        for line in self.cache:
            for word in self.keywords:
                if word in line:
                    self.old_line.append((word,line))

    def compare(self):
        self.new_line = []
        # compare the previous website to updated version
        try:
            requests.get(self.URL).raise_for_status()
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
                            self.new_line.append((word,line))
            self.cache = new
            with open((my_path + str(self.companypage) + '.p'), 'wb') as f:
                pickle.dump(self.cache, f)
        except:
            warnings.warn(self.companypage + ' webpage down')

    def alert(self):
        self.new_line.reverse()
        for line in self.old_line:
            if line in self.new_line:
                self.new_line.remove(line)
        if self.new_line:
            self.new_line.reverse()
            self.message = ["New updates at " + self.companypage + ':' + '\r\n' + '<br>' + self.URL + '<br>']
            print(self.URL)
            for line in self.new_line:
                print(line)
                self.message.append("<b>" + line[0] + "</b>:" + line[1])

    def createMessage(self):
        if self.new_line:
            return ''.join(self.message)