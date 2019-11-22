from abc import ABCMeta, abstractmethod
import re
import os
import time
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import sys
from amal.user_agents import random_ua

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as F_options
from selenium.webdriver.chrome.options import Options as C_options
from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException , NoSuchElementException
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

from multiprocessing import Pool

# put all the Dirty works here
# Don't let the code fool you
# its always dirty

class Scraper(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def _get_item_code(self):
        if self._browser == 'firefox':
            if self._proxy_pool is not None:
                print('using Proxy !')
                browser = webdriver.Firefox(firefox_options=self.options, desired_capabilities=self._proxy_generator())
            else:
                browser = webdriver.Firefox(firefox_options=self.options)  
        elif self._browser == 'chrome':
            if self._proxy_pool is not None:
                print('using Proxy !')
                browser = webdriver.Chrome(chrome_options= self.options, desired_capabilities=self._proxy_generator())
            else:
                browser = webdriver.Chrome(chrome_options= self.options)

        browser.get(self.url)
        try:
            myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
        except TimeoutException:
            print ("Loading took too much time!")
            browser = self.check_robot_and_fix_page(browser)
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

    @abstractmethod
    def check_robot_and_fix_page(self, browser):
        pass

    def _create_worker(self, url):
        if self._proxy_pool is not None:
            worker = Worker(url, self.class_, browser = self._browser,capabilites=self._proxy_generator())
        else:
            worker = Worker(url, self.class_, browser = self._browser)
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
        # with Pool(5) as p:
        #     item_infos = p.map(self._create_worker, list_urls)
        # return item_infos

        item_infos = []
        for link in list_urls:
            item_infos.append(self._create_worker(link))
        return item_infos

    def check_robot_and_fix_page(self, browser):
        while True:
            captcha = browser.find_element_by_css_selector(self.ITEMS_XPATH.CAPTCHA)
            if captcha.get_attribute('src'):
                print('Robot Detected By Amazon !')
                print('captcha link is :', captcha.get_attribute('src'))
                captcha_url = captcha.get_attribute('src')
                img = Image.open(BytesIO(requests.get(captcha_url).content)).convert('L')
                img.save("captcha/captcha.png", "PNG")
                print('image saved to the captcha folder as captcha.png file !')
                captch_input = input('please look at the catpcha and enter it here !').strip()
                captch_elem = browser.find_element_by_css_selector(self.ITEMS_XPATH.CAPTCHA_INPUT)
                captch_elem.send_keys(captch_input)
                captch_elem.send_keys(Keys.RETURN)
                time.sleep(5)
                try:
                    myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
                except TimeoutException:
                    print ("Incorrect Captch Try Again !")
                    continue
                return browser


class AlibabaScraper(Scraper):

    def __init__(self):
        super().__init__()

    def _get_item_code(self):
        browser = super()._get_item_code()

        # adding sleep time to let page load for atleast 10 sec
        time.sleep(10)

        # try:
        #     myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
        # except TimeoutException:
        #     print ("Loading took too much time!")
        # try:
        #     elem = browser.find_element_by_css_selector(self.ITEM_CODE_TAGS['refresh'])
        #     elem.click()
        # except NoSuchElementException as e:
        #     print("didn't found elemnts dom to pass items through !")

        # actions = ActionChains(browser)      
        # actions.key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()
        # # looks like something is wrong with this site
        # # lets try with scrolling first and scraping second
        # # I think they are trying to prevent scraping by bots
        # # if they dont see anyhuman like interaction
        # # they are freezing dom

        # browser.execute_script("window.scrollTo(0, 2900)")
        # time.sleep(10)
        
        # for elem in browser.find_elements_by_xpath(f'//{self.ITEM_CODE_TAGS["element"]}'):
        #     result_ = self._check_element_tags(self.ITEM_CODE_TAGS["tags"], elem)
        #     if result_:
        #         code_ = elem.get_attribute(self.ITEM_CODE_TAGS["value"])
        #         product = re.compile(f"^{self.ITEM_PAGE}.*$").match(code_)
        #         if product is not None:
        #             yield code_.split('?')[0]

        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')

        for tag in soup.find_all('div', {'class':'item-content'}):
            product = tag.find('h2').find('a', href= True)['href'].split('?')[0]
            if not product.startswith('http:'):
                yield 'http:'+product
            else:
                yield product

        for tag in soup.find_all('div', {'data-content': 'abox-ProductNormalList'}):
            product = tag.find('a', href = True)['href'].split('?')[0]
            if not product.startswith('http:'):
                yield 'http:'+product
            else:
                yield product

        browser.close()


    def _scrape_items_info(self):
        list_urls = self.ITEM_CODES
        item_infos = []
        # with Pool(4) as p:
        #     item_infos = p.map(self._create_worker, list_urls)
        for url in list_urls:
            print('scraping link: ' ,url )
            item_infos.append(self._create_worker(url))

        return item_infos

    def check_robot_and_fix_page(self, browser):
        pass

# concept of worker
# 1 worker is one browser instance of slenium webdriver to paralalize the scraping process
# Scraper will initiate worker with multiprocessing library
# proxy options will be built later on

class Worker(object):
    
    def __init__(self, url , target, browser = 'chrome', capabilites = None):

        self._target = target
        if browser == 'chrome':
            self.options = C_options()
            self.create_browser_options()
            if capabilites is not None:
                self._worker = webdriver.Chrome(chrome_options= self.options, desired_capabilities= capabilites)
            else:
                self._worker = webdriver.Chrome(chrome_options= self.options)
        elif browser == 'firefox':
            self.options = F_options()
            self.create_browser_options()
            if capabilites is not None:
                self._worker = webdriver.Firefox(firefox_options= self.options, desired_capabilities= capabilites)
            else:
                self._worker = webdriver.Firefox(firefox_options= self.options)

        self._worker.get(url)

    def create_browser_options(self):
        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        self.user_data_path = os.path.join(self._tmp_folder, 'user-data/')

        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)

        self.data_path = os.path.join(self._tmp_folder, 'data-path/')

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.cache_dir = os.path.join(self._tmp_folder, 'cache-dir/')

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        self.options.add_argument('--enable-logging')
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1280x1696')
        self.options.add_argument('--user-data-dir={}'.format(self.user_data_path))
        self.options.add_argument('--hide-scrollbars')
        self.options.add_argument('--v=99')
        self.options.add_argument('--single-process')
        self.options.add_argument('--data-path={}'.format(self.data_path))
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--homedir={}'.format(self._tmp_folder))
        self.options.add_argument('--disk-cache-dir={}'.format(self.cache_dir))
        self.options.add_argument('user-agent={}'.format(random_ua))


    def work(self, scraper_pathClass):
        # some of the links might not have the pereferred attributes
        product = self.find_element_by_css(scraper_pathClass.PRODUCT_X_PATH)
        price = self.find_element_by_css(scraper_pathClass.PRICE_X_PATH)
        rate = self.find_element_by_css(scraper_pathClass.PRODUCT_PRICE_RATE_X_PATH)
        info = self.find_element_by_css(scraper_pathClass.PRODUCT_INFO_X_PATH)

        return {'item_name': product, 'price': price, 'rate': rate, 'info': info}

    def find_element_by_css(self, css_selector):
        try:
            val = self._worker.find_element_by_css_selector(css_selector).text
        except NoSuchElementException as e:
            self.robot_check()
            val = None
        return val

    def robot_check(self):
        if self._target == 'AMAZON':
            while True:
                captcha = self._worker.find_element_by_css_selector('div.a-row:nth-child(2) > img:nth-child(1)')
                if captcha.get_attribute('src'):
                    print('Robot Detected By Amazon !')
                    print('captcha link is :', captcha.get_attribute('src'))
                    captcha_url = captcha.get_attribute('src')
                    img = Image.open(BytesIO(requests.get(captcha_url).content)).convert('L')
                    img.save("captcha/captcha.png", "PNG")
                    print('image saved to the captcha folder as captcha.png file !')
                    captch_input = input('please look at the catpcha and enter it here !').strip()
                    captch_elem = self._worker.find_element_by_css_selector('#captchacharacters')
                    captch_elem.send_keys(captch_input)
                    captch_elem.send_keys(Keys.RETURN)
                    time.sleep(5)
                    try:
                        myElem = WebDriverWait(self._worker, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_TAB)))
                    except TimeoutException:
                        print ("Incorrect Captch Try Again !")
                        continue
                    break
        else:
            pass

    def close(self):
        self._worker.close()
