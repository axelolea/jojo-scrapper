from constants.models import Character, Stand
from bs4 import BeautifulSoup
import re


def get_basic_data(
        obj: Character | Stand,
        soup: BeautifulSoup,
        card: BeautifulSoup
) -> Character | Stand:
    # <-- Object Name -->
    obj.name = card.select_one('[data-source="title"]').string

    # <-- Object Japanese Name -->
    obj.japanese_name = card.select_one('[lang=ja]').text

    # <-- Object Parts -->
    urls_list = [
        url.attrs['href']
        for url in soup.select('div#catlinks a')
    ]
    obj.parts = get_parts(urls_list)

    # <-- Half Body -->
    if images_half := card.select('div[data-source="image"] .tabber__panel'):
        obj.images.half_body = images_half[0].find('img').attrs['src']
        for img in images_half:
            if img.attrs['data-title'] == 'Anime':
                obj.images.half_body = img.find('img').attrs['src']
                break
    else:
        obj.images.half_body = None

    # <-- Full Body -->
    if images_full := soup.select('div.tbox img'):
        obj.images.full_body = images_full[-1].attrs['src']
    elif images_full := soup.select_one('.mw-header + div.floatleft img'):
        obj.images.full_body = images_full.attrs['src']
    else:
        obj.images.full_body = None

    return obj


def get_parts(
        urls: list
) -> list:

    return [
        int(
            re.search(r'\d', url).group()
        )
        for url in urls
        if re.search(r'/Category:Part_\d_Characters', url)
    ]
