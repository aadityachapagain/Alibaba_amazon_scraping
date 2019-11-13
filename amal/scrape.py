from abc import ABCMeta, abstractmethod
import re
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException , NoSuchElementException
from selenium.webdriver import ActionChains

from multiprocessing import Pool

# put all the Dirty works here
# Don't let the code fool you
# its always dirty

class Scraper(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def _get_item_code(self):
        browser = webdriver.Firefox(firefox_options=self.options)
        browser.get(self.url)
        try:
            myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
        except TimeoutException:
            print ("Loading took too much time!")
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
    def _scrape_items_info(self, item_code):
        pass

    def _create_worker(self, url):
        worker = Worker(url)
        values = worker.work(self.ITEMS_XPATH)
        worker.close()
        del worker
        return values


class AmazonScraper(Scraper):

    def __init__(self):
        super().__init__()


    def _get_item_code(self):
        browser = super()._get_item_code()
        try:
            myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
        except TimeoutException:
            print ("Loading took too much time!")
        for elem in browser.find_elements_by_xpath(f'//{self.ITEM_CODE_TAGS["element"]}'):
            result_ = self._check_element_tags(self.ITEM_CODE_TAGS["tags"], elem)
            if result_:
                code_ = elem.get_attribute(self.ITEM_CODE_TAGS["value"])
                if len(code_):
                    yield code_
        browser.close()


    def _scrape_items_info(self):
        list_urls = map(lambda x: f'{self.ITEM_PAGE}{x}' ,self.ITEM_CODES)
        with Pool(5) as p:
            item_infos = p.map(self._create_worker, list_urls)
        return item_infos

        # item_infos = []
        # for link in list_urls:
        #     item_infos.append(self._create_worker(link))
        # return item_infos

class AlibabaScraper(Scraper):

    def __init__(self):
        super().__init__()

    def _get_item_code(self):
        browser = super()._get_item_code()
        browser.get(self.url)
        try:
            myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
        except TimeoutException:
            print ("Loading took too much time!")
        try:
            elem = browser.find_element_by_css_selector(self.ITEM_CODE_TAGS['refresh'])
            elem.click()
        except NoSuchElementException as e:
            print("didn't found elemnts dom to pass items through !")

        actions = ActionChains(browser)      
        actions.key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()
        # looks like something is wrong with this site
        # lets try with scrolling first and scraping second
        # I think they are trying to prevent scraping by bots
        # if they dont see anyhuman like interaction
        # they are freezing dom

        browser.execute_script("window.scrollTo(0, 2900)")
        time.sleep(10)
        
        for elem in browser.find_elements_by_xpath(f'//{self.ITEM_CODE_TAGS["element"]}'):
            result_ = self._check_element_tags(self.ITEM_CODE_TAGS["tags"], elem)
            if result_:
                code_ = elem.get_attribute(self.ITEM_CODE_TAGS["value"])
                product = re.compile(f"^{self.ITEM_PAGE}.*$").match(code_)
                if product is not None:
                    yield code_.split('?')[0]
        browser.close()


    def _scrape_items_info(self):
        list_urls = self.ITEM_CODES

        with Pool(5) as p:
            item_infos = p.map(self._create_worker, list_urls)
        return item_infos


# concept of worker
# 1 worker is one browser instance of slenium webdriver to paralalize the scraping process
# Scraper will initiate worker with multiprocessing library
# proxy options will be built later on

class Worker(object):
    
    def __init__(self, url):
        self.options = Options()
        self.options.add_argument("--headless")

        self._worker = webdriver.Firefox(firefox_options=self.options)
        self._worker.get(url)

    def work(self, scraper_pathClass):
        # some of the links might not have the pereferred attributes
        product = self.find_element_by_css(scraper_pathClass.PRODUCT_X_PATH).text
        price = self.find_element_by_css(scraper_pathClass.PRICE_X_PATH).text
        rate = self.find_element_by_css(scraper_pathClass.PRODUCT_PRICE_RATE_X_PATH).text
        info = self.find_element_by_css(scraper_pathClass.PRODUCT_INFO_X_PATH).text

        return {'item_name': product, 'price': price, 'rate': rate, 'info': info}

    def find_element_by_css(self, css_selector):
        try:
            val = self._worker.find_element_by_css_selector(css_selector).text
        except NoSuchElementException as e:
            print(e)
            val = 'NA'
        return val

    def close(self):
        self._worker.close()
