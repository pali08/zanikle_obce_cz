import os, sys
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def soupfindAllnSave(pagefolder, url, soup, tag2find='img', inner='src'):
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
            if not os.path.isfile(filepath):  # was not downloaded
                with open(filepath, 'wb') as file:
                    filebin = session.get(fileurl)
                    # filebin = requests.Session().get(fileurl)
                    file.write(filebin.content)
        except Exception as exc:
            print(exc, file=sys.stderr)
    return soup


def savePage(response, pagefilename='page'):
    url = response.url
    response.encoding='windows-1250'
    soup = BeautifulSoup(response.text)
    print(soup.original_encoding)
    pagefolder = pagefilename + '_files'  # page contents
    soup = soupfindAllnSave(pagefolder, url, soup, 'img', inner='src')
    soup = soupfindAllnSave(pagefolder, url, soup, 'link', inner='href')
    soup = soupfindAllnSave(pagefolder, url, soup, 'script', inner='src')
    print(type(soup))
    with open(pagefilename + '.html', mode='w', encoding='windows-1250') as file:
        file.write(soup.decode_contents(eventual_encoding='windows-1250'))
    return soup


# example how to download page:
session = requests.Session()
# #... whatever requests config you need here
response = session.get('http://www.zanikleobce.cz/index.php?obec=1')
savePage(response, '/home/pali/zan_obc')
