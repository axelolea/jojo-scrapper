from constants.models import Character, Stand
from bs4 import BeautifulSoup


def get_basic_data(
        obj: Character | Stand,
        soup: BeautifulSoup,
        card: BeautifulSoup
) -> Character | Stand:

    # <-- Character Name -->
    obj.name = card.select_one('[data-source="title"]').string

    # <-- Character Japanese Name -->
    obj.japanese_name = card.select_one('[lang=ja]').text

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
    if images_full := soup.select('.mw-header + div.floatleft'):
        pass
    elif images_full := soup.select('div.tbox img'):
        pass
    else:
        obj.images.full_body = None

    # image_url = images_full[0].find('img').attrs['src']
    # for img in images_container:
    #     if img.attrs['data-title'] == 'Anime':
    #         image_url = img.find('img').attrs['src']
    #         break
    # obj.half_body = image_url
    # try:
    #     obj.full_body = soup.select_one('div.floatleft') \
    #         .find('img').attrs['src']

    return obj


def get_parts(soup: BeautifulSoup) -> list:
    parts_list = list()
    parts = soup.select('div#catlinks a')
    return parts_list
