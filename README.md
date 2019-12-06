# Aliama (Scraping Alibaba and Amazon)

## What is Aliama ?

It is a platform for easy scraping of amazon item price, weight and many more.

### Features

- [x] Collect AMSIN of items from amazon
- [x] Collect the product information from asin code.
- [X] Add options to add proxy during scraping.
- [X] create random proxy scraper to automate the scraping with different proxies.

### Using the code.

* clone the Repository 
* Download [Chrome WebDriver](https://chromedriver.chromium.org/) and [Firefox webdriver](https://github.com/mozilla/geckodriver/releases)
* Unzip and Make both Driver Executable and move them to system path for ubuntu move them to `/usr/local/bin`

```python

#without proxy

from amal import Alibaba, Amazon

scraper_ins = Amazon(m_item)
#  to get the item code from amazon and alibaba
scraper_ins.get_item_code()
# scraped results
product_lists = scraper_ins.scrape()

```

```python

#Using proxy

# create proxy generator function
from amal import Alibaba, Amazon
import random
import socket

def proxy_generator():
    username = 'proxy-username-id'
    password = 'prxy-pass'
    port = 22225
    super_proxy = socket.gethostbyname('zproxy.domain.io')
    url = "http://%s-session-%s:%s@"+super_proxy+":%d"
    while True:
        session_id = random.random()
        yield url % (username, session_id, password,port)


scraper_ins = Amazon(m_item, proxy_generator= proxy_generator)
#  to get the item code from amazon and alibaba
scraper_ins.get_item_code()
# scraped results
product_lists = scraper_ins.scrape()

```

### Finally

That's it . Finally Done!