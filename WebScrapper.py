from bs4 import BeautifulSoup as BS
import requests
from selenium import webdriver



class WebScrapper:

    def __init__(self):
        
        self.req = requests
        self.browser = webdriver.Firefox()

    def scrapp_Bus(self,url =  "https://www.tmb.cat/es/transporte-barcelona/servicio-metro-bus/estado-red-bus", parser = 'html.parser'):

        page = self.browser.get(url)
        soup = BS(page.page_source,parser)
        print(soup.prettify())
        mydivs = soup.find_all("div",{"class": "network__line"})
        print(mydivs)


if __name__ == '__main__':
    sc = WebScrapper()
    sc.scrapp_Bus()