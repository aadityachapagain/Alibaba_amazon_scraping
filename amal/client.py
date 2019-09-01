# import library
from abc import ABCMeta, abstractmethod

# import modules
from amal.urls import ALIBABA_URL, AMAZON_URL, ALIBABA_SEARCH_TAB, AMAZON_ITEMS_PAGE, ALIBABA_ITEMS_PAGE, AMAZON_SEARCH_TAB
from amal.urls import AMAZON_ITEM_CODE_TAGS, ALIBABA_ITEM_CODE_TAGS

class Client(metaclass= ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

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

    
    def scrape(self):
        return super().scrape()

    def get_item_code(self):
        self._get_item_code()


class AlibabaClient(Client):

    def __init__(self, item_name):
        super().__init__()
        self.url = ALIBABA_URL
        self.item_name = item_name
        self.class_ = "ALIBABA"
        self.SEARCH_TAB = ALIBABA_SEARCH_TAB
        self.ITEM_CODE_TAGS = ALIBABA_ITEM_CODE_TAGS
        self.ITEM_PAGE = ALIBABA_ITEMS_PAGE

    def scrape(self):
        return super().scrape()

    def get_item_code(self):
        self._get_item_code()