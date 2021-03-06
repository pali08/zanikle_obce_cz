import os, sys
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def soup_find_all_and_save(pagefolder, url, soup, tag2find='img', inner='src'):
    if not os.path.exists(pagefolder):  # create only once
        os.mkdir(pagefolder)
    for res in soup.findAll(tag2find):  # images, css, etc..
        try:
            filename = os.path.basename(res[inner])
            fileurl = urljoin(url, res.get(inner))
            # rename to saved file path
            # res[inner] # may or may not exist
            filepath = os.path.join(pagefolder, filename)
            res[inner] = os.path.join(os.path.basename(pagefolder), filename)
            session = requests.Session()
            if not os.path.isfile(filepath):  # was not downloaded
                with open(filepath, 'wb') as file:
                    filebin = session.get(fileurl)
                    file.write(filebin.content)
        except Exception as exc:
            print(exc, file=sys.stderr)
    return soup


def get_page(response, pagefilename='page'):
    url = response.url
    response.encoding = 'windows-1250'
    soup = BeautifulSoup(response.text)
    pagefolder = pagefilename + '_files'  # page contents
    soup = soup_find_all_and_save(pagefolder, url, soup, 'img', inner='src')
    soup = soup_find_all_and_save(pagefolder, url, soup, 'link', inner='href')
    soup = soup_find_all_and_save(pagefolder, url, soup, 'script', inner='src')
    return soup


def save_page(response, pagefilename='page'):
    soup = get_page(response, pagefilename)
    with open(pagefilename + '.html', mode='w', encoding='utf-8') as file:
        file.write(soup.decode_contents(eventual_encoding='utf-8'))
