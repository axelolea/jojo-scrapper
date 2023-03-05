from bs4 import BeautifulSoup
from requests import Session
from constanst import Character, Images, DOMAIN, FOLDER_NAME
import re

session = Session()


def fetch(url:str) -> str:
    resp = session.get(url)
    content = resp.content
    return BeautifulSoup(content, 'html.parser')

def get_users(url:str):
    # Create requeste a page 
    soup = fetch(url)
    return [ DOMAIN + item.attrs["href"] for item in soup.select('div#mw-pages a')]

from constanst import RIPPLE_LINK, SPIN_LINK

ripple_users = get_users(RIPPLE_LINK)
spin_users = get_users(SPIN_LINK)


def get_character_data(obj: dict) -> Character:
    try:
        # Create Character Object 
        char = Character()
        # Create requeste a page 
        soup = fetch(obj['page'])

        card = soup.select_one('aside.portable-infobox')

        char.url = obj['page']
        char.id = obj['id']
        # <-- Character Name -->
        char.name = card.select_one('h2[data-source="title"]').string
        # <-- Character Japanese Name -->
        char.japanese_name = card.select_one('div[data-source="ja_kanji"] [lang=ja]').text
        # <-- Character Set parts -->
        char.parts = obj['parts']
        # <-- Character Catchphrase -->
        try:
            slogan = soup.find('div', class_='cquote').text
            slogan = re.sub(r'\n', '', slogan)
            slogan = re.search(r'“.*?”', slogan)
            slogan = re.sub(r'(“|”)', '', slogan.string())
        except:
            slogan = None
            # .find('div', id = 'nihongo').text
        # char.catchphrase = re.search(r'', slogan)
        char.catchphrase = slogan

        # <-- Character Alias -->
        try:
            alias_items = card.select('div[data-source="alias"] div, div[data-source="engname"] div')
            char.alther_name = ', '.join([item.text for item in alias_items])
        except:
            char.alther_name = None

        # <-- Character Stands -->

        try:
            stands = card.select_one('div[data-source="stand"]')
            char.stands = [stand.attrs['href'] for stand in stands.find_all('a')] if stands else None
        except:
            char.stands = None
        
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
        species = card.select_one('div[data-source="species"] div')
        if species:
            char.is_human = False
        else:
            char.is_human = True
        # <-- Character ripple user -->
        char.is_hamon_user = True if char.url in ripple_users else False
        # <-- Character spin user -->
        char.is_gyro_user = True if char.url in spin_users else False
        # <-- Print Result -->
        print(char)
        return char
    except:
        return obj['page']


# <-- Create data files -->

import json
import os
import pandas as pd
from constanst import Character

def create_files(characters_list:list[Character]):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame([char.__dict__ for char in characters_list])
    # df.to_excel( FOLDER_NAME + 'character.xlsx')
    # df.to_csv( FOLDER_NAME + 'character.csv')
    parsed = json.loads(df.to_json(orient="records"))
    with open(FOLDER_NAME + 'data.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)