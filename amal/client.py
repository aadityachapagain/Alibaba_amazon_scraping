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


class AmazonClient(Client):

    def __init__(self):
        super().__init__()

    
    def scrape(self):
        return super().scrape()

    def get_item_code(self, item_name):
        return super().get_item_code(item_name)


class AlibabaClient(Client):

    def __init__(self):
        super().__init__()

    def scrape(self):
        return super().scrape()

    def get_item_code(self, item_name):
        return super().get_item_code(item_name)