from re import sub, search
from constants.constants import DOMAIN
from constants.models import Character
from scrapper import get_scrapper

from get_data.basic_data import get_basic_data

scrapper = get_scrapper()


def get_users_list(url: str) -> list:
    # Create requests a page
    soup = scrapper.fetch(url)
    return [DOMAIN + item.attrs["href"] for item in soup.select('div#mw-pages a')]


RIPPLE_USERS = get_users_list(DOMAIN + '/Category:Ripple_Users')
SPIN_USERS = get_users_list(DOMAIN + '/Category:Spin_Users')


def get_character_data(url_search: str) -> Character:
    # <-- Get soup -->
    soup = scrapper.fetch(url_search)
    # <-- Get card -->
    card = soup.select_one('aside.portable-infobox')

    # <-- Character Basics -->
    basic_data = get_basic_data(
        soup,
        card
    )

    # <-- Create Character Object -->
    char = Character(**basic_data
                     )

    char.url = url_search

    # <-- Character Catchphrase -->
    if slogan := soup.select_one('div.cquote'):
        slogan = sub(r'\n', '', slogan.text)
        slogan = search(r'“.*?”', slogan)
        char.catchphrase = sub(r'[“”]', '', slogan.group())
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
    country = card.select_one('div[data-source="nation"] img')
    char.country = country.attrs['alt'] if country else None

    # <-- Character Living -->
    death = card.select_one('div[data-source="death"]')
    char.living = False if death else True

    # <-- Character isHuman -->
    char.is_human = False if card.select_one('[data-source="species"]') else True

    # <-- Character ripple user -->
    char.is_ripple_user = True if char.url in RIPPLE_USERS else False

    # <-- Character spin user -->
    char.is_spin_user = True if char.url in SPIN_USERS else False

    # <-- Print Result -->
    print(char)
    return char
