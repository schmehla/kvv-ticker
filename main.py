from bs4 import BeautifulSoup
import requests
import sys
import re
from jinja2 import Template

from hash_tree import *
from notify import *

URL = 'https://www.kvv.de/fahrplan/verkehrsmeldungen.html'
MAIL_PATTERN = '[^@]+@[^@]+.\w+'
FILTER_CHARS = '[a-zA-Z0-9_\-\ ,]'
ARG_PATTERN = '^(' + MAIL_PATTERN + ')(?:\{((?:' + FILTER_CHARS + '+(?:\||&))*)(' + FILTER_CHARS + '+)\})?$'

def run():
    if not arguments_valid():
        return
    html_page = requests.get(URL)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    results = soup.find_all('div', class_='ix_kvv_ticker_list')
    hash_tree = HashTree(results)
    diffs = hash_tree.find_diffs()
    if len(diffs) < 1:
        print('[INFO] nothing new')
        return
    hash_tree.update()
    table = transform_diffs_to_table(diffs)
    for arg in sys.argv[1:]:
        matches = re.match(ARG_PATTERN, arg)
        email_adr = matches.group(1)
        if matches.group(2) and matches.group(3):
            filters = matches.group(2) + matches.group(3)
            table = filter_table(table, filters)
            if len(table) < 1:
                continue
        response_page = build_response_page(table)
        send_email('Aktuelle Verkehrsmeldungen', 'KVV Ticker', response_page, email_adr)

def transform_diffs_to_table(diffs):
    table = []
    for diff in diffs:
        dict_ = {
            'date': diff.find('span', class_='date').text,
            'subject': diff.find('h3', class_='ticker_subject').text,
            'content': diff.find('p').text,
            'details_link': 'https://www.kvv.de' + diff.find('a', class_='internal-link')['href']
        }
        table.append(dict_)
    return table

def filter_table(table, filters):
    def contains_all(string, substring_list):
        for substring in substring_list:
            if not substring in string:
                return False
        return True
    
    filtered_table = []
    for row in table:
        joined_row = row['subject'] + row['content']
        for and_filters in filters.split('|'):
            if contains_all(joined_row, and_filters.split('&')):
                filtered_table.append(row)
                break
    return filtered_table

def build_response_page(table):
    with open('template.html') as f:
        template = Template(f.read())
    return template.render(table=table)

def arguments_valid():
    if len(sys.argv) < 2:
        print('[ERROR] arguments are missing')
        return False
    for arg in sys.argv[1:]:
        matches = re.match(ARG_PATTERN, arg)
        if not matches:
            print('[ERROR] incorrect argument pattern, use mail@domain.com{string1|string2&string3} (& binds stronger than |)')
            return False
    return True

if __name__ == '__main__':
    run()