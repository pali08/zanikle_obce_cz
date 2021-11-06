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
    table = soup.find('table').findNext('table').findAll('tr')[2].findAll('td')[0].findAll('div')[0]
    # print(table.prettify())
    basic_info_dict = {}
    category_found = False
    basic_info_dict['name'] = table.find('big').find('b').find('a', href=True).contents[0].strip().replace('\'', '`')
    # basic_info_dict.update(table.find('big').find('b').find('a', href=True).contents[0])
    for b in table.findAll('b'):
        for a in b.findAll('a', href=True):
            # print("Found the URL:", a['href'])
            # print(a.contents[0])
            href_in_anchor = str(a['href'])
            if 'index.php?menu=11&typ=' in href_in_anchor:
                # print(a['href'])
                # print(a.contents[0])
                basic_info_dict.update({'category': a.contents[0]})
                if '(správní obec:'.lower() in b.next_sibling:
                    basic_info_dict.update({'municipality': b.find_next_sibling('b').contents[0].replace('\'', '`')})
                    # print(b.find_next_sibling('b').contents[0])
                    # print('next sibling is: {}'.format(b.next_sibling))
            if 'index.php?menu=11&okr=' in href_in_anchor:
                basic_info_dict.update({'district': a.contents[0].replace('\'', '`')})
            if 'index.php?menu=11&duv=' in href_in_anchor:
                basic_info_dict.update({'end_reason': a.contents[0].replace('\'', '`')})
            if 'index.php?menu=11&obd=' in href_in_anchor:
                basic_info_dict.update({'end_years': a.contents[0].replace('\'', '`')})
            if 'index.php?menu=11&stv=' in href_in_anchor:
                basic_info_dict.update({'actual_state': a.contents[0].replace('\'', '`')})

            # print(a['href'])
            # if '&typ=' in str(a['href']):
            #     try:
            #         print(a['title'])
            #         if a['title'] != 'Interaktivní mapa':
            #             basic_info_dict.update({'category': a.contents[0]})
            #             category_found = True
            #     except KeyError:
            #         continue
            # print(basic_info_dict)
    return basic_info_dict


def get_coordinates(soup):
    table = soup.find('table').findNext('table').findNext('table')
    row_with_halves = table.findAll('tr')[0]
    row_with_coords = table.findAll('tr')[1]
    north_south = row_with_halves.findAll('td')[1].text.split(' ')[-1].split('(')[0]
    north_south_coords = row_with_coords.findAll('td')[1].text.split(' ')[-1].split('(')[0]
    east_west = row_with_halves.findAll('td')[2].text.split(' ')[-1].split('(')[0]
    east_west_coords = row_with_coords.findAll('td')[2].text.split(' ')[-1].split('(')[0]
    return {north_south: float(north_south_coords), east_west: float(east_west_coords)}


def get_images(soup):
    """
    :param soup:
    :return:
    todo later
    """
    pass


def get_data_of_place(address):
    soup = get_soup(address)
    info = get_basic_info(soup)
    try:
        coords = get_coordinates(soup)
        info.update(coords)
    except IndexError:
        info.update({'N': 'NULL', 'E': 'NULL'})
        print('No coordinates for {}, {}'.format(address, info['name']))
    return info
    # print(get_coordinates(soup))
    # print(get_basic_info(soup).prettify())
    # print(next(table))
    # print(table)

# get_data_of_place('http://www.zanikleobce.cz/index.php?obec=25787')
# print(get_data_of_place('http://www.zanikleobce.cz/index.php?obec=26519'))
