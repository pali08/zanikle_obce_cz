import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://www.zanikleobce.cz/index.php?obec=1'
# response = requests.get(url)

# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.title)
#
# tables = soup.findAll('table')
# for table in tables:
#     print(title.text)
# print(len(table))

# tables = pd.read_html(url)
#
# wanted_table = tables[2]
#
# print(wanted_table[2][1])
# print(wanted_table[1][1])


from pywebcopy import save_webpage

# url = 'http://some-site.com/some-page.html'
download_folder = '.'

kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}

save_webpage(url, download_folder, **kwargs)