import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

from page_download_2 import savePage

url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=1'
url_main = 'http://www.zanikleobce.cz/'


# print(table)

# links_lost_places = []
counter = 0
for i in range(1,2):
    url = 'http://www.zanikleobce.cz/index.php?menu=93&sort=1&l=&str=' + str(i)
    response = requests.get(url)
    print(response.encoding)
    print('fuuuck')
    soup = BeautifulSoup(response.text, 'html.parser')
    table_lost_places = soup.find('table')
    for tr in table_lost_places.findAll("tr"):
        # print(tr)
        tds = tr.findAll("td")
        # print(trs[0])
        try:
            link = tds[0].find('a')['href']
            if 'obec=' in link:
                counter += 1
                session = requests.Session()
                response = session.get(url_main + link)
                savePage(response, '/home/pali/PycharmProjects/zanikle_obce_cz/test_subdatabase/item' + str(counter))
                # links_lost_places.append(url_main + link)
        except Exception as any_exception:
            print('Exceotion occured:' + str(any_exception))


