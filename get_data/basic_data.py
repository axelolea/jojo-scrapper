from bs4 import BeautifulSoup
from constants.constants import months
import datetime
import re


def get_basic_data(
        soup: BeautifulSoup,
        card: BeautifulSoup
) -> dict:
    basic_data = dict()

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

    basic_data['images'] = dict()

    # <-- Half Body -->
    if images_half := card.select('div[data-source="image"] .tabber__panel'):
        basic_data['images']['half_body'] = images_half[0].find('img').attrs['src']
        for img in images_half:
            if img.attrs['data-title'] == 'Anime':
                basic_data['images']['half_body'] = img.find('img').attrs['src']
                break
    else:
        basic_data['images']['half_body'] = None

    # <-- Full Body -->
    if images_full := soup.select('div.tbox img'):
        basic_data['images']['full_body'] = images_full[-1].attrs['src']
    elif images_full := soup.select_one('.mw-header + div.floatleft img'):
        basic_data['images']['full_body'] = images_full.attrs['src']
    else:
        basic_data['images']['full_body'] = None

    # <-- Get Last Update
    date_str = soup.select_one('li#footer-info-lastmod').string
    basic_data['last_update'] = get_last_update(date_str)

    return basic_data


def get_parts(urls: list) -> list:
    return [
        int(re.search(r'\d', url).group())
        for url in urls
        if re.search(r'/Category:Part_\d.(Stands|Characters)', url)
    ]


def get_date(date_str: str) -> datetime.datetime:
    date_list = re.search(r'\d{1,2}\s\w+\s\d{4}', date_str)\
        .group().split(' ')
    date_list[1] = months[date_list[1]]
    date_list = [int(date) for date in date_list]
    date_list.reverse()
    return datetime.datetime(*date_list)


def get_last_update(date_str: str) -> float:
    last_date = get_date(date_str)
    return last_date.timestamp()
