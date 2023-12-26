import requests
import sys
import re
from get_apis import get_apis
from bs4 import BeautifulSoup


def make_request(url: str)-> str:
    """
        Use requests module to make URL request and return decoded response.
    """
    sesh = requests.Session()
    response = sesh.get(url)
    return response.content.decode('utf-8')


def using_gtags(resp: str) -> bool:
    """
        Parse html to determine if website is using Google Tag Manager.
    """
    gtag = False
    if resp.__contains__('GTM'):
        gtag = True
    elif resp.__contains__('Google Tag Manager'):
        gtag = True
    elif resp.__contains__('gtag'):
        gtag = True
    return gtag


def parse_response(resp: str) -> tuple:
    """
        Parse html for GTM tags and 
        use helper functions to find container IDs. 
        Returns list of html tags and dictionary with IDs. 
    """
    tags = []
    ids = {}
    soup = BeautifulSoup(resp, "lxml")

    elms = soup.find_all('script')

    for each in elms:
        if str(each).__contains__('gtm.js'):
            tags.append(each)
            tagID = find_tagID(str(each))
            ids["tagID"] = tagID
        elif str(each).__contains__('gtag'):
            tags.append(each)
            gaID = find_gaID(str(each))
            ids["gaID"] = gaID
        elif str(each).__contains__('googletagmanager'):
            tags.append(each)

    elms2 = soup.find_all('noscript')
    if len(elms2) > 0:
        tags.append(elms2)

    return tags, ids

def find_tagID(elm: str) -> list:
    """
        Find Google Tag Manager container ID with regex
    """
    return re.findall(r"GTM-[A-Z0-9]+", elm)

def find_gaID(elm: str) -> list:
    """
        Find GA4 container ID with regex
    """
    return re.findall(r"G-[A-Z0-9]+", elm)


if __name__ == "__main__":
    #args = sys.argv
    #url = args[1]
    url = 'http://marketingisbs.marketing/'
    response = make_request(url)
    if using_gtags(response):
        tags, ids = parse_response(response)
        get_apis(url)
    else:
        print("Google tags not detected")
