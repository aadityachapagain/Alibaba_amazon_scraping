# import library
from abc import ABCMeta, abstractmethod
from selenium.webdriver.firefox.options import Options

# import modules
from amal.urls import ALIBABA_URL, AMAZON_URL, ALIBABA_SEARCH_TAB, AMAZON_ITEMS_PAGE, ALIBABA_ITEMS_PAGE, AMAZON_SEARCH_TAB
from amal.urls import AMAZON_ITEM_CODE_TAGS, ALIBABA_ITEM_CODE_TAGS
from amal.urls import AmazonItemsPaths, AlibabaItemsPaths

class Client(metaclass= ABCMeta):

    def __init__(self):
        # options related to the selenium
        self.options = Options() 
        self.options.add_argument("--headless")

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def get_item_code(self):
        pass


class AmazonClient(Client):

    def __init__(self, item_name):
        super().__init__()
        self.url = AMAZON_URL
        self.item_name = item_name
        self.class_ = "AMAZON"
        self.SEARCH_TAB = AMAZON_SEARCH_TAB
        self.ITEM_CODE_TAGS = AMAZON_ITEM_CODE_TAGS
        self.ITEM_PAGE =  AMAZON_ITEMS_PAGE
        self.ITEMS_XPATH = AmazonItemsPaths

        self.ITEM_CODES = []

    
    def scrape(self):
        return self.scrape_items_info()

    def get_item_code(self):
        self.ITEM_CODES = self._get_item_code()


class AlibabaClient(Client):

    def __init__(self, item_name):
        super().__init__()
        self.url = ALIBABA_URL
        self.item_name = item_name
        self.class_ = "ALIBABA"
        self.SEARCH_TAB = ALIBABA_SEARCH_TAB
        self.ITEM_CODE_TAGS = ALIBABA_ITEM_CODE_TAGS
        self.ITEM_PAGE = ALIBABA_ITEMS_PAGE
        self.ITEMS_XPATH = AlibabaItemsPaths

        self.ITEM_CODES = []


    def scrape(self):
        return self.scrape_items_info()

    def get_item_code(self):
        self.ITEM_CODES = self._get_item_code()