from constanst import Character, Stand
from bs4 import BeautifulSoup


def get_basic_data(
        obj: Character | Stand,
        soup: BeautifulSoup,
        card: BeautifulSoup
    ) -> Character | Stand:
    # <-- Half Body -->

    images_container = card.select_one('div[data-source="image"]')
    try:
        images_half = images_container.select('.tabber__panel')

        obj.half_body = images_half[0].find('img').attrs['src']

        for img in images_half:
            if img.attrs['data-title'] == 'Anime':
                obj.half_body = img.find('img').attrs['src']
                break
    except:
        obj.half_body = images_container.select_one('a.image img').attrs['src']
    # <-- Full Body -->
    try:
        images_full = soup.select_one('div.tbox') \
            .select('article.tabber__panel')
        image_url = images_full[0].find('img').attrs['src']

        for img in images_container:
            if img.attrs['data-title'] == 'Anime':
                image_url = img.find('img').attrs['src']
                break

    finally:
        obj.half_body = image_url
    full_image = soup.select_one('div.floatleft')
    obj.full_body = full_image if full_image.find('img').attrs['src'] else None

    return obj
