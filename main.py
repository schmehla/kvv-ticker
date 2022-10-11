from bs4 import BeautifulSoup
import requests
import sys
from jinja2 import Template

from hash_tree import *
from notify import *

URL = 'https://www.kvv.de/fahrplan/verkehrsmeldungen.html'

def run():
    html_page = requests.get(URL)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    results = soup.find_all('div', class_='ix_kvv_ticker_list')
    hash_tree = HashTree(results)
    diffs = hash_tree.find_diffs()
    if len(diffs) < 1:
        return
    hash_tree.update()
    response_page = build_response_page(diffs)
    for email_adr in sys.argv[1:]:
        send_email('Aktuelle Verkehrsmeldungen', 'KVV Ticker', response_page, email_adr)

    

def build_response_page(diffs):
    dict_diffs = []
    for diff in diffs:
        dict_ = {
            'date': diff.find('span', class_='date').text,
            'subject': diff.find('h3', class_='ticker_subject').text,
            'content': diff.find('p').text,
            'details_link': 'https://www.kvv.de' + diff.find('a', class_='internal-link')['href']
        }
        dict_diffs.append(dict_)
    with open('template.html') as f:
        template = Template(f.read())
    return template.render(diffs=dict_diffs)

if __name__ == '__main__':
    run()