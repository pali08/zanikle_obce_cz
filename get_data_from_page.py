import requests
from bs4 import BeautifulSoup


def get_soup(webpage_address):
    response = requests.get(webpage_address)
    # url = response.url
    response.encoding = 'windows-1250'
    return BeautifulSoup(response.text, 'html.parser')
    # return BeautifulSoup(response.text, 'html.parser')
    # pass


def get_basic_info(soup):
    pass


def get_coordinates(soup):
    table = soup.find('table').findNext('table').findNext('table')
    row_with_halves = table.findAll('tr')[0]
    row_with_coords = table.findAll('tr')[1]
    north_south = row_with_halves.findAll('td')[1].text.split(' ')[-1].split('(')[0]
    north_south_coords = row_with_coords.findAll('td')[1].text.split(' ')[-1].split('(')[0]
    east_west = row_with_halves.findAll('td')[2].text.split(' ')[-1].split('(')[0]
    east_west_coords = row_with_coords.findAll('td')[2].text.split(' ')[-1].split('(')[0]
    return {north_south: float(north_south_coords), east_west: float(east_west_coords)}


def get_other_articles(soup):
    pass


def get_comments(soup):
    pass


def get_images(soup):
    """
    :param soup:
    :return:
    todo later
    """
    pass


def get_data_from_page(address):
    soup = get_soup(address)
    print(get_coordinates(soup))
    # print(next(table))
    # print(table)


get_data_from_page('http://www.zanikleobce.cz/index.php?obec=28139')
