from constants.models import Stand
from get_data.basic_data import get_basic_data
from constants.constants import STATS_DATA_SOURCE, STATS_REGEX
from scrapper import get_scrapper

import re

scrapper = get_scrapper()


def get_stand_data(url_search: str) -> Stand | None:
    # <-- Create requests a page -->
    soup = scrapper.fetch(url_search)
    # <-- Create card -->
    card = soup.select_one('aside.portable-infobox')

    try:
        basic_data = get_basic_data(
            soup,
            card
        )
    except:
        return None

    # <-- Create Stand Object -->
    stand = Stand(**basic_data)

    stand.url = url_search

    # <-- Stand Battle-cry -->

    stand_cry = card.select_one('[data-source="cry"] div')
    cry_strings = stand_cry.contents if stand_cry else None
    if stand_cry:
        stand.battle_cry = ' '.join([cry for cry in cry_strings if isinstance(cry, str)])
    else:
        stand.battle_cry = None
    # <-- Stand Alias -->

    alias_items = card.select('div[data-source="engname"] div')
    stand.alter_name = ', '.join([item.text for item in alias_items]) if alias_items else None

    # <-- Stand abilities -->
    abilities = soup.select('[href="#Abilities"] + ul span[class="toctext"]')
    stand.abilities = ', '.join([item.text for item in abilities])

    # <-- Stand Stats -->

    stats = {}

    for stat in STATS_DATA_SOURCE:
        if stat_value := card.select_one(f'td[data-source="{stat}"]'):
            stats[stat] = re.search(STATS_REGEX, stat_value.text).group()
        else:
            stats[stat] = '?'

    stand.stats.__dict__.update(**stats)

    # <-- Print Result -->
    # print(stand)
    return stand
