# import library
from abc import ABCMeta, abstractmethod

# import modules
from amal.urls import ALIBABA_URL, AMAZON_URL, ALIBABA_SEARCH_TAB, AMAZON_ITEMS_PAGE, ALIBABA_SEARCH_TAB

class Client(metaclass= ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def get_item_code(self, item_name):
        pass