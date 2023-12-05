import requests
import sys
from bs4 import BeautifulSoup


def make_request(url: str)-> str:
    sesh = requests.Session()
    response = sesh.get(url)
    return response.content.decode('utf-8')


def using_gtags(resp: str) -> bool:
    gtag = False
    if resp.__contains__('GTM'):
        gtag = True
    elif resp.__contains__('Google Tag Manager'):
        gtag = True
    elif resp.__contains__('gtag'):
        gtag = True
    return gtag


def parse_response(resp: str):
    tags = []
    soup = BeautifulSoup(resp, "lxml")

    elms = soup.find_all('script')

    for each in elms:
        if str(each).__contains__('gtm.js'):
            tags.append(each)
        elif str(each).__contains__('gtag'):
            tags.append(each)
        elif str(each).__contains__('googletagmanager'):
            tags.append(each)

    elms2 = soup.find_all('noscript')
    if len(elms2) > 0:
        tags.append(elms2)

    return tags


def get_apis():
    pass


if __name__ == "__main__":
    #args = sys.argv
    #url = args[1]
    url = 'http://marketingisbs.marketing'
    response = make_request(url)
    if using_gtags(response):
        tags = parse_response(response)

    # add lots of custom tags
    # look for those tag elements in page resources being downloaded on page initialization
