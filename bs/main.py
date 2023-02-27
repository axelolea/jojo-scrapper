import requests
from bs4 import BeautifulSoup
from threading import Thread
import concurrent.futures
from itertools import islice
from constanst import DOMAIN, MAX_PARTS, FOLDER_NAME, Images, N_THREADS


def run():
    parts_pages = [f'{DOMAIN}/Category:Part_{i}_Characters' for i in range(1, MAX_PARTS + 1)]

    characters_pages = list()
    # <-- Get all characters pages -->
    for number, page in enumerate(parts_pages, start=1):
        resp = requests.get(page)
        content = resp.content
        soup = BeautifulSoup(content, 'html.parser')
        character_tags = soup.select_one('div.diamond2').select('div.charname a')
        characters_pages.extend([{'page': DOMAIN + tag.attrs["href"], 'parts': [number,]} for tag in character_tags])

    # <-- Delete all duplicate pages -->

    duplicated_pages = list()

    for index, page in enumerate(characters_pages):
        if index in duplicated_pages:
            continue
        comp_list = characters_pages[index + 1: len(characters_pages)]
        for comp_index, comp_page in enumerate(comp_list, start=index + 1):
            if page['page'] == comp_page['page']:
                characters_pages[index]['parts'].extend(characters_pages[comp_index]['parts'])
                duplicated_pages.append(comp_index)
    duplicated_pages.sort(reverse=True)
    for index in duplicated_pages:
        characters_pages.pop(index)

    # <-- Get info of all characters -->

    characters = list()
    error_characters = list()

    for obj in characters_pages:
        try:
            character =  get_character_data(obj['page'])
            character.parts = obj['parts']
            characters.append(character)
        except:
            error_characters.append(obj['page'])
    create_files(characters)
    for page in error_characters:
        print(f'<< Error: {page} >>')
    # threads = list()
    # with concurrent.futures.ThreadPoolExecutor() as Executor:

    #     pass
    # for _ in range(1, N_THREADS + 1):
    #     t = Thread(target=get_character_data, args=[page])
    #     t.start
    #     threads.append(t)
    # for thread in threads:
    #     thread.join()

from constanst import Character
import re

def get_character_data(url: str) -> Character:
    # Create Character Object 
    char = Character()
    # Create requeste a page 
    resp = requests.get(url)
    content = resp.content
    soup = BeautifulSoup(content, 'html.parser')

    card = soup.select_one('aside.portable-infobox')

    # <-- Character Name -->
    char.name = card.select_one('h2[data-source="title"]').string

    # <-- Character Catchphrase -->
    slogan = soup.find('div', class_='cquote').text
        # .find('div', id = 'nihongo').text
    # char.catchphrase = re.search(r'', slogan)
    char.catchphrase = slogan

    # <-- Character Japanese Name -->
    char.japanese_name = card.select_one('div[data-source="ja_kanji"] [lang=ja]').text

    # <-- Character Alias -->
    alias_items = card.select('div[data-source="alias"], div[data-source="engname"]')
    if not alias_items:
        char.alther_name = None
    else:
        char.alther_name = ', '.join([item.find('div').text for item in alias_items])

    # <-- Character Stands -->
    stands = card.select_one('div[data-source="stand"]')
    char.stands = [stand.attrs['href'] for stand in stands.find_all('a')] if stands else None
    
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
        images.full_body = soup.select_one('div.floatleft')\
            .find('img').attrs['src']

    char.images = images
    # <-- Character Country -->
    char.url = url
    char.is_hamon_user = False
    char.is_gyro_user = False
    char.is_human = True
    # print(soup.title)
    print(char)
    return char

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
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    with open(FOLDER_NAME + 'data.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)

# Run Main func

if __name__ == '__main__':
    run()