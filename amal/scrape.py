from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# put all the Dirty works here

class Scraper(metaclass=ABCMeta):

    def __init__(self):
        self._item_codes = []
        self.options = Options()  
        self.options.add_argument("--headless")  

    @abstractmethod
    def _get_item_code(self):
        browser = webdriver.Firefox(firefox_options=options)
        browser.get(self.url)
        elem = browser.find_element_by_css_selector(self.SEARCH_TAB)
        elem.send_keys(self.item_name)
        elem.send_keys(Keys.RETURN)
        return browser

class AmazonScraper(Scraper):

    def __init__(self):
        super().__init__()

    def _get_item_code(self):
        browser = super()._get_item_code()

# concept of worker
# 1 worker is one browser instance of slenium webdriver to paralalize the scraping process
# Scraper will initiate worker with multiprocessing library
class Worker(object):
    
    def __init__(self, url):
        self._url = url