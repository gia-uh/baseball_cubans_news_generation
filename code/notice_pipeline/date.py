import requests
from bs4 import Comment
from bs4 import BeautifulSoup

PARSER = 'lxml'
try:
    import lxml
except ImportError:
    PARSER = 'html.parser'

def get_date():
    with requests.Session() as ss:
        ss.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'
        ss.headers['Accept-Encoding'] = 'gzip, deflate'
        base_url = 'https://baseball-reference.com'
        r = ss.get(base_url)
        bsObj = BeautifulSoup(r.text, PARSER)
        date = bsObj.find('div', {'id': 'scores'}).h2.a['href']
    return date.replace('/boxes/?date=', '')

#print(get_date())