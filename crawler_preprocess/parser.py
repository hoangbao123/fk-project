import pprint
import time

import requests
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)


# Request XML data from link and parse it with BeautifulSoup
def returnCoolXML(url):
    heads = {'Accept-Language': 'en-US',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
             'Connection': 'keep-alive', 'Referer': '216.58.220.196'}
    while (True):
        try:
            req = requests.get(url, headers=heads)
        except requests.exceptions.ConnectionError as e:
            print("Conncetion Error. Trying again.")
            time.sleep(1.2)
            continue
        break
    time.sleep(0.5)
    data = BeautifulSoup(req.text, "xml")
    req.close()
    time.sleep(0.4)
    return data


# Request HTML data from link and parse it with BeautifulSoup
def returnCoolHTML(url):
    heads = {'Accept-Language': 'en-US',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
             'Connection': 'keep-alive', 'Referer': '216.58.220.196'}
    while (True):
        try:
            req = requests.get(url, headers=heads)
        except requests.exceptions.ConnectionError as e:
            print("Conncetion Error. Trying again.")
            time.sleep(1.2)
            continue
        break
    data = BeautifulSoup(req.text, "html5lib")
    req.close()
    return data