import re
from constanst import (
    fetch,
    Character,
    Stand,
    DOMAIN,
    FOLDER_NAME
)


def get_stand_data(obj: dict) -> Stand:
    try:
        # Create Stand Object

        stand = Stand()

        # Create requests a page

        soup = fetch(obj['url'])

        card = soup.select_one('aside.portable-infobox')

        stand.url = obj['url']
        stand.id = obj['id']

        # <-- Stand Name -->

        stand.name = card.select_one('[data-source="title"]').string

        # <-- Stand Japanese Name -->

        stand.japanese_name = card.select_one('[lang=ja]').text

        # <-- Stand Set parts -->

        stand.parts = obj['parts']

        # <-- Stand Battle-cry -->

        stand_cry = card.select_one('[data-source="cry"] div')
        stand.battle_cry = stand_cry.contents if stand_cry else None

        # <-- Stand Alias -->

        alias_items = card.select('div[data-source="engname"] div')
        stand.alter_name = ', '.join([item.text for item in alias_items]) if alias_items else None

        # <-- Stand abilities -->
        abilities = soup.select('[href="#Abilities"] + ul span[class="toctext"]')
        stand.abilities = ', '.join([item.text for item in abilities])

        stand.stats.power = card.select_one('td[data-source="destpower"]').text
        stand.stats.speed = card.select_one('td[data-source="speed"]').text
        stand.stats.range = card.select_one('td[data-source="range"]').text
        stand.stats.durability = card.select_one('td[data-source="stamina"]').text
        stand.stats.precision = card.select_one('td[data-source="precision"]').text
        stand.stats.potential = card.select_one('td[data-source="potential"]').text

        # <-- Half Body -->

        images_container = card.select_one('div[data-source="image"]')
        try:
            images_half = images_container.select('.tabber__panel')

            stand.half_body = images_half[0].find('img').attrs['src']

            for img in images_half:
                if img.attrs['data-title'] == 'Anime':
                    stand.half_body = img.find('img').attrs['src']
                    break
        except:
            stand.half_body = images_container.select_one('a.image img').attrs['src']
        # <-- Full Body -->
        try:
            images_full = soup.select_one('div.tbox') \
                .select('article.tabber__panel')
            image_url = images_full[0].find('img').attrs['src']

            for img in images_container:
                if img.attrs['data-title'] == 'Anime':
                    image_url = img.find('img').attrs['src']
                    break
            stand.half_body = image_url
        except:
            try:
                stand.full_body = soup.select_one('div.floatleft') \
                    .find('img').attrs['src']
            except:
                stand.full_body = None

        # <-- Print Result -->

        print(stand)

        return stand

    except Exception as e:
        print('<!-- ---------- Error ---------- -->')
        print(f'Type: {type(e)}, Args: {e.args}, Exception: {e}, Url: {obj["url"]}')