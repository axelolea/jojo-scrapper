import re
from constanst import (
    fetch,
    Character,
    Stand,
    Images,
    Stats,
    DOMAIN,
    FOLDER_NAME
)


def get_users_list(url: str) -> list:
    # Create requests a page
    soup = fetch(url)
    return [DOMAIN + item.attrs["href"] for item in soup.select('div#mw-pages a')]


RIPPLE_USERS = get_users_list(DOMAIN + '/Category:Ripple_Users')
SPIN_USERS = get_users_list(DOMAIN + '/Category:Spin_Users')


def get_character_data(obj: dict) -> Character:
    try:
        # Create Character Object 

        char = Character()

        # Create requests a page
        url_search = obj['url']
        soup = fetch(url_search)

        card = soup.select_one('aside.portable-infobox')

        char.url = url_search
        char.id = obj['id']

        # <-- Character Name -->

        char.name = card.select_one('[data-source="title"]').string

        # <-- Character Japanese Name -->

        char.japanese_name = card.select_one('[lang=ja]').text

        # <-- Character Set parts -->

        char.parts = obj['parts']

        # <-- Character Catchphrase -->

        if slogan := soup.select_one('div.cquote'):
            slogan = re.sub(r'\n', '', slogan.text)
            slogan = re.search(r'“.*?”', slogan)
            char.catchphrase = re.sub(r'[“”]', '', slogan.group())
        else:
            char.catchphrase = None

        # <-- Character Alias -->

        alias_items = card.select('div[data-source="alias"] div, div[data-source="engname"] div')
        char.alter_name = ', '.join([item.text for item in alias_items]) if alias_items else None

        # <-- Character Stands -->

        stands = card.select_one('[data-source="stand"]')
        char.stands = [
            stand.attrs['href']
            for stand in stands.find_all('a')
        ] if stands else None

        # <-- Character Country -->
        try:
            char.country = card.select_one('div[data-source="nation"] img').attrs['alt']
        except:
            char.country = None

        # <-- Character Living -->
        death = card.select_one('div[data-source="death"]')
        char.living = False if death else True

        # <-- Half Body -->

        images_container = card.select_one('div[data-source="image"]')
        try:
            images_half = images_container.select('.tabber__panel')

            char.half_body = images_half[0].find('img').attrs['src']

            for img in images_half:
                if img.attrs['data-title'] == 'Anime':
                    char.half_body = img.find('img').attrs['src']
                    break
        except:
            char.half_body = images_container.select_one('a.image img').attrs['src']
        # <-- Full Body -->
        try:
            images_full = soup.select_one('div.tbox') \
                .select('article.tabber__panel')
            image_url = images_full[0].find('img').attrs['src']

            for img in images_container:
                if img.attrs['data-title'] == 'Anime':
                    image_url = img.find('img').attrs['src']
                    break
            char.half_body = image_url
        except:
            try:
                char.full_body = soup.select_one('div.floatleft') \
                    .find('img').attrs['src']
            except:
                char.full_body = None


        # <-- Character isHuman -->

        char.is_human = False if card.select_one('[data-source="species"]') else True

        # <-- Character ripple user -->

        char.is_ripple_user = True if char.url in RIPPLE_USERS else False

        # <-- Character spin user -->

        char.is_spin_user = True if char.url in SPIN_USERS else False

        # <-- Print Result -->

        print(char)

        return char

    except Exception as e:
        print(f'Type: {type(e)}, Args: {e.args}, Exception: {e}, Url: {obj["url"]}')


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


# <-- Create data files -->

import json
import os
import pandas as pd
from constanst import Character


def create_files(items_list: list[Character], filename: str):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame([item.__dict__ for item in items_list])
    # df.to_excel( FOLDER_NAME + 'character.xlsx')
    # df.to_csv( FOLDER_NAME + 'character.csv')
    parsed = json.loads(df.to_json(orient="records"))
    with open(FOLDER_NAME + f'{filename}.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)
