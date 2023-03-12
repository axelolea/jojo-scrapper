from constants.constants import fetch
from constants.models import Stand
from get_data.basic_data import get_basic_data


def get_stand_data(url_search: str) -> Stand:
    # <-- Create Stand Object -->
    stand = Stand()
    # <-- Create requests a page -->
    soup = fetch(url_search)
    # <-- Create card -->
    card = soup.select_one('aside.portable-infobox')

    get_basic_data(
        stand,
        soup,
        card
    )

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

    stand.stats.power = card.select_one('td[data-source="destpower"]').text
    stand.stats.speed = card.select_one('td[data-source="speed"]').text
    stand.stats.range = card.select_one('td[data-source="range"]').text
    stand.stats.durability = card.select_one('td[data-source="stamina"]').text
    stand.stats.precision = card.select_one('td[data-source="precision"]').text
    stand.stats.potential = card.select_one('td[data-source="potential"]').text

    stand.stats.clean_stats()
    # <-- Print Result -->
    print(stand)
    return stand

