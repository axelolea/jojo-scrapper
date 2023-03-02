from bs4 import BeautifulSoup
from requests import Session
from constanst import DOMAIN, MAX_PARTS, FOLDER_NAME, Images
from concurrent.futures import ThreadPoolExecutor
from itertools import islice

session = Session()
characters = list()


def run():
    parts_pages = [f'{DOMAIN}/Category:Part_{i}_Characters' for i in range(1, MAX_PARTS + 1)]

    characters_obj = list()
    # <-- Get all characters pages -->
    for number, page in enumerate(parts_pages, start=1):
        resp = session.get(page)
        content = resp.content
        soup = BeautifulSoup(content, 'html.parser')
        character_tags = soup.select_one('div.diamond2').select('div.charname a')
        characters_obj.extend([{'page': DOMAIN + tag.attrs["href"], 'parts': [number,]} for tag in character_tags])

    # <-- Delete all duplicate pages -->

    duplicated_pages = set()

    for index, item in enumerate(characters_obj):
        if index in duplicated_pages:
            continue
        comp_list = characters_obj[index + 1: len(characters_obj)]
        for comp_index, comp in enumerate(comp_list, start=index + 1):
            if item['page'] == comp['page']:
                characters_obj[index]['parts'].extend(characters_obj[comp_index]['parts'])
                duplicated_pages.add(comp_index)
    characters_obj = [item for index, item in enumerate(characters_obj) if index not in duplicated_pages]
    print(len(characters_obj))
    # <-- Get info of all characters -->

    with ThreadPoolExecutor() as executor:
        executor.map(get_character_data, characters_obj)
    # for page in error_characters:
    #     print(f'<< Error: {page} >>')


from constanst import Character
import re

def get_character_data(obj: dict) -> Character:

    # Create Character Object 
    char = Character()
    # Set parts in obj
    char.parts = obj['parts']
    # Create requeste a page 
    resp = session.get(obj['page'])
    content = resp.content
    soup = BeautifulSoup(content, 'html.parser')

    card = soup.select_one('aside.portable-infobox')

    # <-- Character Name -->
    char.name = card.select_one('h2[data-source="title"]').string
    # <-- Character Catchphrase -->
    try:
        slogan = soup.find('div', class_='cquote').text
        slogan = re.sub(r'\n', '', slogan)
        slogan = re.search(r'“.*?”', slogan)
        slogan = re.sub(r'(“|”)', '', slogan[0])
    except:
        slogan = None
        # .find('div', id = 'nihongo').text
    # char.catchphrase = re.search(r'', slogan)
    char.catchphrase = slogan

    # <-- Character Japanese Name -->
    char.japanese_name = card.select_one('div[data-source="ja_kanji"] [lang=ja]').text

    # <-- Character Alias -->
    try:
        alias_items = card.select('div[data-source="alias"], div[data-source="engname"]')
        if not alias_items:
            char.alther_name = None
        else:
            char.alther_name = ', '.join([item.find('div').text for item in alias_items])
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
        nation = card.select_one('div[data-source="nation"]')
        char.country = nation.find('img').attrs['alt'] if nation else None
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
        
        image_url = images_half[0].find('img').attrs['src']
        
        for img in images_container:
            if img.attrs['data-title'] == 'Anime':
                image_url = img.find('img').attrs['src']
                break
        images.half_body = image_url
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

    char.images = images
    # <-- Character Country -->
    char.url = obj['page']
    char.is_hamon_user = False
    char.is_gyro_user = False
    char.is_human = True
    print(char)
    characters.append(char)
    return

# <-- Create data files -->

import json
import os
import pandas as pd

def create_files(characters_list:list[Character]):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame([char.__dict__ for char in characters_list])
    df.to_excel( FOLDER_NAME + 'character.xlsx')
    df.to_csv( FOLDER_NAME + 'character.csv')
    parsed = json.loads(df.to_json(orient="records"))
    with open(FOLDER_NAME + 'data.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)

# Run Main func

if __name__ == '__main__':
    run()
    create_files(characters)