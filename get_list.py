from get_data.characters import fetch
from constants.constants import DOMAIN, MAX_PARTS, FOLDER_NAME
from constants.models import Character, Stand
import os
import json
import pandas as pd

TABLE_CHARACTERS_PAGES = [
    f'{DOMAIN}/Category:Part_{num}_Characters'
    for num in range(1, MAX_PARTS + 1)
]


def get_characters_pages() -> set:

    characters_set = set()

    # <-- Get all characters pages -->
    for page in TABLE_CHARACTERS_PAGES:
        soup = fetch(page)
        character_tags = soup.select_one('div.diamond2').select('div.charname a')
        for tag in character_tags:
            char_url = f'{DOMAIN}{tag.attrs["href"]}'
            characters_set.add(char_url)

    return characters_set


def get_stands_pages() -> set:
    stands_list = set()
    soup = fetch(f'{DOMAIN}/List_of_Stands')
    table_stands_pages = soup.select('div.diamond2')

    # <-- Get all characters pages -->

    for block in table_stands_pages[:MAX_PARTS - 2]:
        stands_tags = block.select('div.charname a')
        for tag in stands_tags:
            stand_url = f'{DOMAIN}{tag.attrs["href"]}'
            stands_list.add(stand_url)

    # <-- Delete all duplicate pages -->

    return stands_list


def create_files(items_list: list[Character | Stand], filename: str):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame([item.__dict__ for item in items_list])
    parsed = json.loads(df.to_json(orient="records"))
    with open(FOLDER_NAME + f'{filename}.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)
