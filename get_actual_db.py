import traceback

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

from page_download_2 import savePage

url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
url_main = 'http://www.zanikleobce.cz/'


# print(table)

def get_number_of_pages():
    url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_lost_places = soup.find('table')
    highest_page = 0
    for tr in table_lost_places.findAll("tr"):
        tds = tr.findAll("td")
        try:
            table_inside = tds[0].find('table')
            for tr in table_inside.findAll('tr'):
                for td in tr.findAll('td'):
                    for div in td.findAll('div'):
                        for link in div.findAll('a'):
                            if 'str=' in link['href']:
                                if int(link['href'].rsplit('str=')[1]) > highest_page:
                                    highest_page = int(link['href'].rsplit('str=')[1])
        except AttributeError as attr_error:
            pass
        except Exception as any_exception:
            print('Exception occurred:' + str(any_exception) + 'stack trace follows')
            print(traceback.format_exc())
    return highest_page


def get_database_of_lost_places():
    num_of_pages = get_number_of_pages()
    counter = 0
    for i in range(1, num_of_pages + 1):
        url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=' + str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_lost_places = soup.find('table')
        for tr in table_lost_places.findAll("tr"):
            tds = tr.findAll("td")
            try:
                link = tds[0].find('a')['href']
                if 'obec=' in link:
                    counter += 1
                    session = requests.Session()
                    response = session.get(url_main + link)
                    savePage(response,
                             '/media/pali/8F0A-DF4B/zanikle_obce/item_{:05d}'.format(counter))
            except AttributeError as attr_error:
                pass
            except Exception as any_exception:
                print('Exception occurred:' + str(any_exception) + 'stack trace follows')
                print(traceback.format_exc())


get_database_of_lost_places()
