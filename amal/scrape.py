from abc import ABCMeta, abstractmethod
import re

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
        browser = webdriver.Firefox(firefox_options=self.options)
        browser.get(self.url)
        elem = browser.find_element_by_css_selector(self.SEARCH_TAB)
        elem.send_keys(self.item_name)
        elem.send_keys(Keys.RETURN)
        return browser


    def _check_element_tags(self, tags, elem):
        for tag in tags:
            if elem.get_attribute(tag) is None:
                return False
        return True

    @abstractmethod
    def scrape_item_info(self, item_code):
        pass

class AmazonScraper(Scraper):

    def __init__(self):
        super().__init__()


    def _get_item_code(self):
        browser = super()._get_item_code()
        for elem in browser.find_elements_by_xpath(f'//{self.ITEM_CODE_TAGS["element"]}'):
            result_ = self._check_element_tags(self.ITEM_CODE_TAGS["tags"], elem)
            if result_:
                code_ = elem.get_attribute(self.ITEM_CODE_TAGS["value"])
                product = re.compile(f"^{self.ITEM_PAGE}.*$").match(code_)
                if product is not None:
                    self._item_codes.append(code_)


    def scrape_item_info(self, item_code):
        return super().scrape_item_info(item_code)


class AlibabaScraper(Scraper):

    def __init__(self):
        super().__init__()

    def _get_item_code(self):
        browser = super()._get_item_code()
        for elem in browser.find_elements_by_xpath(f'//{self.ITEM_CODE_TAGS["element"]}'):
            result_ = self._check_element_tags(self.ITEM_CODE_TAGS["tags"], elem)
            if result_:
                code_ = elem.get_attribute(self.ITEM_CODE_TAGS["value"])
                self._item_codes.append(code_)


    def scrape_item_info(self, item_code):
        return super().scrape_item_info(item_code)

# concept of worker
# 1 worker is one browser instance of slenium webdriver to paralalize the scraping process
# Scraper will initiate worker with multiprocessing library
class Worker(object):
    
    def __init__(self, url):
        self._url = url