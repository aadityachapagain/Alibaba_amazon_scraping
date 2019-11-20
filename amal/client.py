# import library
from abc import ABCMeta, abstractmethod
from selenium.webdriver.firefox.options import Options as F_options
from selenium.webdriver.chrome.options import Options as C_options
from selenium.common.exceptions import UnknownMethodException

# Using proxy
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType


# import modules
from amal.urls import ALIBABA_URL, AMAZON_URL, ALIBABA_SEARCH_TAB, AMAZON_ITEMS_PAGE, ALIBABA_ITEMS_PAGE, AMAZON_SEARCH_TAB
from amal.urls import AMAZON_ITEM_CODE_TAGS, ALIBABA_ITEM_CODE_TAGS
from amal.urls import AmazonItemsPaths, AlibabaItemsPaths

class Client(metaclass= ABCMeta):

    def __init__(self, proxy_pool = None,browser = 'chrome'):
        # options related to the selenium
        if proxy_pool is not None:
            self._proxy_pool = proxy_pool()
        self._proxy_pool = None
        if browser == 'chrome':
            self.options = C_options()
        elif browser == 'firefox':
            self.options == F_options()
        else:
            raise UnknownMethodException(f'Wrong browser name {browser}')
        
        self.options.add_argument("log-level=3")
        self.options.add_argument("--headless")
        self._browser = browser

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def get_item_code(self):
        pass

    def _proxy_generator(self):
        "Randomly generate the deliberate proxy !"
        if self._browser == 'chrome':
            _capabilities = DesiredCapabilities.CHROME
        else:
            _capabilities = DesiredCapabilities.FIREFOX
        _proxy = Proxy()
        _proxy.proxy_type = ProxyType.MANUAL
        _proxy.http_proxy = next(self._proxy_pool)
        _proxy.ssl_proxy = next(self._proxy_pool)
        _proxy.add_to_capabilities(_capabilities)

        return _capabilities


class AmazonClient(Client):

    def __init__(self, item_name, proxy_pool = None, browser = 'chrome'):
        
        """
        item_name: Name of item you want to scrape information of
        proxy_pool: proxy_pool function
                    user provided function which will randomly generate correct proxy urls
                    (function must be iterator)
        browser: --headless browser you want to use to scrape items using
        """

        super().__init__(proxy_pool=proxy_pool, browser= browser)
        self.url = AMAZON_URL
        self.item_name = item_name
        self.class_ = "AMAZON"
        self.SEARCH_TAB = AMAZON_SEARCH_TAB
        self.ITEM_CODE_TAGS = AMAZON_ITEM_CODE_TAGS
        self.ITEM_PAGE =  AMAZON_ITEMS_PAGE
        self.ITEMS_XPATH = AmazonItemsPaths

        self.ITEM_CODES = []

    
    def scrape(self):
        scraped_info = self._scrape_items_info()
        return list(filter(lambda x: x['item_name'] != None, scraped_info))

    def get_item_code(self):
        self.ITEM_CODES = list(self._get_item_code())


class AlibabaClient(Client):

    def __init__(self, item_name, proxy_pool = None, browser = 'chrome'):

        """
        item_name: Name of item you want to scrape information of
        proxy_pool: proxy_pool function
                    user provided function which will randomly generate correct proxy urls
                    (function must be iterator)
        browser: --headless browser you want to use to scrape items using
        """

        super().__init__(proxy_pool=proxy_pool, browser= browser)
        self.url = ALIBABA_URL
        self.item_name = item_name
        self.class_ = "ALIBABA"
        self.SEARCH_TAB = ALIBABA_SEARCH_TAB
        self.ITEM_CODE_TAGS = ALIBABA_ITEM_CODE_TAGS
        self.ITEM_PAGE = ALIBABA_ITEMS_PAGE
        self.ITEMS_XPATH = AlibabaItemsPaths

        self.ITEM_CODES = []


    def scrape(self):
        scraped_info = self._scrape_items_info()
        return list(filter(lambda x: x['item_name'] != None, scraped_info))

    def get_item_code(self):
        self.ITEM_CODES = list(self._get_item_code())