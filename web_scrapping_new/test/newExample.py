from bs4 import BeautifulSoup
import requests

class MyClass:

    def __init__(self, text):
        self.text = text

    def show(self):
        print("hello {}".format(self.text))
