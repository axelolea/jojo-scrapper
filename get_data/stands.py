from constants.models import Stand
from get_data.basic_data import get_basic_data
from scrapper import get_scrapper
import re

scrapper = get_scrapper()


def get_stand_data(url_search: str) -> Stand:
    # <-- Create requests a page -->
    soup = scrapper.fetch(url_search)
    # <-- Create card -->
    card = soup.select_one('aside.portable-infobox')

    basic_data = get_basic_data(
        soup,
        card
    )

    # <-- Create Stand Object -->
    stand = Stand(**basic_data)

    stand.url = url_search

    # <-- Stand Battle-cry -->

    stand_cry = card.select_one('[data-source="cry"] div')
    stand.battle_cry = stand_cry.contents if stand_cry else None

    # <-- Stand Alias -->

    alias_items = card.select('div[data-source="engname"] div')
    stand.alter_name = ', '.join([item.text for item in alias_items]) if alias_items else None

    # <-- Stand abilities -->
    abilities = soup.select('[href="#Abilities"] + ul span[class="toctext"]')
    stand.abilities = ', '.join([item.text for item in abilities])

    # <-- Stand Stats -->

    stand.stats = {}
    regex = r'Null|A|B|C|D|E|\∞|\?'

    for stat in [
        'destpower',
        'speed',
        'range',
        'stamina',
        'precision',
        'potential'
    ]:
        if stat_value := card.select_one(f'td[data-source="{stat}"]'):
            stand.stats[stat] = re.search(regex, stat_value.text).group()
        else:
            stand.stats[stat] = '?'

    # <-- Print Result -->
    # print(stand)
    return stand
