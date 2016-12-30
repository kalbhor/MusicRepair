'''
Returns Album Art url

Bing search requires API key. (Fetches it from environment varibles)
'''
from . import log
import requests
import json
from bs4 import BeautifulSoup
import six
from os import environ

if six.PY2:
    from urllib2 import urlopen, Request
    from urllib2 import quote
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen, Request

LOG_LINE_SEPERATOR = '........................\n'

try:
    BING_KEY = environ['BING_IMG_KEY']

except KeyError:
    log.log_error('Warning, BING_IMG_KEY not added in environment variables')

def img_search_bing(album):
    ''' Bing image search '''

    album = album + " Album Art"

    api_key = "Key"
    endpoint = "https://api.cognitive.microsoft.com/bing/v5.0/images/search"
    links_dict = {}

    headers = {'Ocp-Apim-Subscription-Key': str(BING_KEY)}
    param = {'q': album, 'count': '1'}

    response = requests.get(endpoint, headers=headers, params=param)
    response = response.json()

    key = 0
    try:
        for i in response['value']:
            links_dict[str(key)] = str((i['contentUrl']))
            key = key + 1

        return links_dict["0"]
        
    except KeyError:
        return None

def img_search_google(album):
    '''
    google image search
    '''

    album = album + " Album Art"
    url = ("https://www.google.com/search?q=" +
           quote(album.encode('utf-8')) + "&source=lnms&tbm=isch")
    header = {'User-Agent':
              '''Mozilla/5.0 (Windows NT 6.1; WOW64)
              AppleWebKit/537.36 (KHTML,like Gecko)
              Chrome/43.0.2357.134 Safari/537.36'''
             }



    soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")

    albumart_div = soup.find("div", {"class": "rg_meta"})
    
    try:
        albumart = json.loads(albumart_div.text)["ou"]
        return albumart
    except:
        pass
    
    return ''

