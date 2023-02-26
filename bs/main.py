import requests
from bs4 import BeautifulSoup


from constanst import DOMAIN, MAX_PARTS, FOLDER_NAME


def run():
    parts_pages = [f'{DOMAIN}/Category:Part_{i}_Characters' for i in range(1, MAX_PARTS + 1)]
    characters = list()
    for page in parts_pages:
        resp = requests.get(page)
        content = resp.content
        soup = BeautifulSoup(content, 'html.parser')
        character_tags = soup.select_one('div.diamond2')\
            .select('div.charname a')
        
        i = 0
        for tag in character_tags:
            page = DOMAIN + tag.attrs["href"]
            character =  get_character_data(page)
            characters.append(character)
            if i > 3:
                break
            i = i + 1
    create_csv(characters)

from constanst import Character
import re

def get_character_data(url: str) -> Character:
    # Create Character Object 
    char = Character()
    # Create requeste a page 
    resp = requests.get(url)
    content = resp.content
    soup = BeautifulSoup(content, 'html.parser')

    card = soup.select_one('aside.portable-infobox'.replace(' ', '.'))

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
    nation = card.select_one('div[data-source="nation"]')
    char.country = nation.find('img').attrs['alt'] if nation else None

    # <-- Character Living -->
    death = card.select_one('div[data-source="death"]')
    char.living = False if death else True

    # <-- Images -->
    
    # <-- Character Country -->
    char.url = url


    print(char)
    return char

# <-- Create data files -->

import json
import os
import pandas as pd

def create_csv(list:list[Character]):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame([char.__dict__ for char in list])
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