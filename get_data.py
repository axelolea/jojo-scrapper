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

def get_users_list(url:str) -> list:
    # Create requeste a page 
    soup = fetch(url)
    return [ DOMAIN + item.attrs["href"] for item in soup.select('div#mw-pages a')]

RIPPLE_USERS = get_users_list(DOMAIN + '/Category:Ripple_Users')
SPIN_USERS = get_users_list(DOMAIN + '/Category:Spin_Users')

def get_character_data(obj: dict) -> Character:
    try:
        # Create Character Object 

        char = Character()

        # Create requeste a page 

        soup = fetch(obj['url'])

        card = soup.select_one('aside.portable-infobox')

        char.url = obj['url']
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
            char.catchphrase = re.sub(r'(“|”)', '', slogan.group())
        else:
            char.catchphrase = None

        # <-- Character Alias -->

        alias_items = card.select('div[data-source="alias"] div, div[data-source="engname"] div')
        char.alther_name = ', '.join([item.text for item in alias_items]) if alias_items else None

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

        # <-- Character Images -->

        images = Images()

        # <-- Half Body -->

        images_container = card.select_one('div[data-source="image"]')
        try:
            images_half = images_container.select('.tabber__panel')
            
            images.half_body = images_half[0].find('img').attrs['src']
            
            for img in images_half:
                if img.attrs['data-title'] == 'Anime':
                    images.half_body = img.find('img').attrs['src']
                    break
        except:
            images.half_body = images_container.select_one('a.image img').attrs['src']
        # <-- Full Body -->
        try:
            images_full = soup.select_one('div.tbox')\
                .select('article.tabber__panel')
            image_url = images_full[0].find('img').attrs['src']
            
            for img in images_container:
                if img.attrs['data-title'] == 'Anime':
                    image_url = img.find('img').attrs['src']
                    break
            images.half_body = image_url
        except:
            try:
                images.full_body = soup.select_one('div.floatleft')\
                    .find('img').attrs['src']
            except:
                images.full_body = None

        # <-- Set images a character -->

        char.images = images

        # <-- Character isHuman -->

        char.is_human = False if card.select_one('[data-source="species"]') else True
        
        # <-- Character ripple user -->

        char.is_hamon_user = True if char.url in RIPPLE_USERS else False

        # <-- Character spin user -->

        char.is_gyro_user = True if char.url in SPIN_USERS else False

        # <-- Print Result -->

        print(char)

        return char
    
    except Exception as e:
        return {
            'type': type(e),
            'args': e.args,
            'exception': e,
            'url': obj['url']
        }
    
def get_stand_data(obj:dict) -> Stand:
    try:
        # Create Stand Object 

        stand = Stand()

        # Create requeste a page 

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

        # <-- Stand Battlecry -->

        stand_cry = card.select_one('[data-source="cry"] div')

        # <-- Stand Alias -->

        alias_items = card.select('div[data-source="engname"] div')
        stand.alther_name = ', '.join([item.text for item in alias_items]) if alias_items else None

        # <-- Stand abilities -->
        abilities = soup.select('[href="#Abilities"] + ul span[class="toctext"]')
        stand.abilities = ', '.join([item.text for item in abilities])

        # <-- Stand stats -->
        stats = Stats()

        stats.power = card.select_one('td[data-source="destpower"]').text
        stats.speed = card.select_one('td[data-source="speed"]').text
        stats.range = card.select_one('td[data-source="range"]').text
        stats.durability = card.select_one('td[data-source="stamina"]').text
        stats.precision = card.select_one('td[data-source="precision"]').text
        stats.potential = card.select_one('td[data-source="potential"]').text

        stand.stats = stats

        # <-- Stand Images -->

        images = Images()

        # <-- Half Body -->

        images_container = card.select_one('div[data-source="image"]')
        try:
            images_half = images_container.select('.tabber__panel')
            
            images.half_body = images_half[0].find('img').attrs['src']
            
            for img in images_half:
                if img.attrs['data-title'] == 'Anime':
                    images.half_body = img.find('img').attrs['src']
                    break
        except:
            images.half_body = images_container.select_one('a.image img').attrs['src']
        # <-- Full Body -->
        try:
            images_full = soup.select_one('div.tbox')\
                .select('article.tabber__panel')
            image_url = images_full[0].find('img').attrs['src']
            
            for img in images_container:
                if img.attrs['data-title'] == 'Anime':
                    image_url = img.find('img').attrs['src']
                    break
            images.half_body = image_url
        except:
            try:
                images.full_body = soup.select_one('div.floatleft')\
                    .find('img').attrs['src']
            except:
                images.full_body = None

        # <-- Set images a Stand -->

        stand.images = images

        # <-- Print Result -->

        print(stand)

        return stand
    
    except Exception as e:
        return {
            'type': type(e),
            'args': e.args,
            'exception': e,
            'url': obj['url']
        }


# <-- Create data files -->

import json
import os
import pandas as pd
from constanst import Character

def create_files(items_list:list[Character], filename:str):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame([item.__dict__ for item in items_list])
    # df.to_excel( FOLDER_NAME + 'character.xlsx')
    # df.to_csv( FOLDER_NAME + 'character.csv')
    parsed = json.loads(df.to_json(orient="records"))
    with open(FOLDER_NAME + f'{filename}.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)