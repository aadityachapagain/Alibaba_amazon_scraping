# -*- coding: utf-8 -*-


"""

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                             _
  __ _   _ __ ___     __ _  | |
 / _` | | '_ ` _ \   / _` | | |
| (_| | | | | | | | | (_| | | |
 \__,_| |_| |_| |_|  \__,_| |_|
                               

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


__version__ = '1.1.0'
__author__ = 'Aaditya Chapagain'

from amal.client import AlibabaClient, AmazonClient
from amal.scrape import AlibabaScraper, AmazonScraper



class Amazon(AmazonClient, AmazonScraper):
    """
    Amazon class is  mixins of both AmazonClient and AmazonScraper,
    This class is becoming to scrape both items imformation and Asin codes
    """

    def __init__(self, item_name):
        super().__init__(item_name)


class Alibaba(AlibabaClient, AlibabaScraper):
    """
    Alibaba class is mixins of both AlibabClient and Alibaba Scraper,
    This class is becoming to scrape both items imformation and links from amazon
    """

    def __init__(self, item_name):
        super().__init__(item_name)