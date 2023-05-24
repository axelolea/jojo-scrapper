from bs4 import BeautifulSoup
from re import search
from constants.utils import get_image_select, get_last_update


def get_basic_data(
        soup: BeautifulSoup,
        card: BeautifulSoup
) -> dict:

    basic_data = dict()

    # <-- Get Last Update
    date_str = soup.select_one('li#footer-info-lastmod').string
    basic_data['last_update'] = get_last_update(date_str)

    # <-- Object Name -->
    basic_data['name'] = card.select_one('[data-source="title"]').string

    # <-- Object Japanese Name -->
    basic_data['japanese_name'] = card.select_one('[lang=ja]').text

    # <-- Object Parts -->
    urls_list = [
        url.attrs['href']
        for url in soup.select('div#catlinks a')
    ]

    basic_data['parts'] = get_parts(urls_list)

    # <-- Images Dict -->
    basic_data['images'] = dict()

    # <-- Half Body -->
    if images_half := card.select('div[data-source="image"] .tabber__panel'):
        basic_data['images']['half_body'] = images_half[0].find('img').attrs['src']
        for img in images_half:
            if img.attrs['data-title'] == 'Anime':
                basic_data['images']['half_body'] = img.find('img').attrs['src']
                break
    else:
        images_half = card.select_one('div[data-source="image"] img')
        basic_data['images']['half_body'] = images_half.attrs['src']

    # <-- Full Body -->
    if images_full := soup.select('div.floatleft img'):
        image_select = get_image_select(len(images_full))
        basic_data['images']['full_body'] = images_full[image_select].attrs['src']
    else:
        basic_data['images']['full_body'] = None

    return basic_data


def get_parts(urls: list) -> list:
    return [
        int(search(r'\d', url).group())
        for url in urls
        if search(r'/Category:Part_\d.(Stands|Characters)', url)
    ]
