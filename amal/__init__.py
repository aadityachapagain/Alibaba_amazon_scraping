# -*- coding: utf-8 -*-

__version__ = '1.2.1'
__author__ = 'Aaditya Chapagain'
__doc__ = """

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                             _
  __ _   _ __ ___     __ _  | |
 / _` | | '_ ` _ \   / _` | | |
| (_| | | | | | | | | (_| | | |
 \__,_| |_| |_| |_|  \__,_| |_|
                               

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Library based on selenium  and proxy handler to scrape item from alibaba and amazon

upgrades:
* Added proxy handlers  [Nov 19]
"""

from amal.client import AlibabaClient, AmazonClient
from amal.scrape import AlibabaScraper, AmazonScraper



class Amazon(AmazonClient, AmazonScraper):
    """
    Amazon class is  mixins of both AmazonClient and AmazonScraper,
    This class is becoming to scrape both items imformation and Asin codes
    """

    def __init__(self, item_name, proxy_generator = None, browser = 'chrome'):

        """
        proxy_generator: proxy_pool function
                    user provided function which will randomly generate correct proxy urls
                    (function must be iterator)
        browser: --headless browser you want to use to scrape items using
        """
        super().__init__(item_name, proxy_pool= proxy_generator, browser = browser)


class Alibaba(AlibabaClient, AlibabaScraper):
    """
    Alibaba class is mixins of both AlibabClient and Alibaba Scraper,
    This class is becoming to scrape both items imformation and links from amazon
    """

    def __init__(self, item_name, proxy_generator = None, browser = 'chrome'):

        """
        proxy_generator: proxy_pool function
                    user provided function which will randomly generate correct proxy urls
                    (function must be iterator)
        browser: --headless browser you want to use to scrape items using
        """

        super().__init__(item_name, proxy_pool= proxy_generator, browser = browser)