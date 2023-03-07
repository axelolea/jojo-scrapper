from constanst import DOMAIN, MAX_PARTS
from get_data import fetch


def remove_repeat(list_items: list) -> list:
    duplicated_pages = set()

    for index, item in enumerate(list_items):

        if index in duplicated_pages:
            continue

        start_index = index + 1
        comp_list = list_items[start_index: len(list_items)]
        # Create comparative list 

        for comp_index, comp in enumerate(comp_list, start=start_index):
            if item['url'] == comp['url']:
                list_items[index]['parts'].extend(list_items[comp_index]['parts'])
                duplicated_pages.add(comp_index)
    return [item for index, item in enumerate(list_items) if index not in duplicated_pages]


def get_characters_list() -> list:
    characters_obj = list()

    mosaic_characters = [
        f'{DOMAIN}/Category:Part_{i}_Characters'
        for i in range(1, MAX_PARTS + 1)
    ]

    # <-- Get all characters pages -->
    for number, page in enumerate(mosaic_characters, start=1):
        soup = fetch(page)
        character_tags = soup.select_one('div.diamond2') \
            .select('div.charname a')
        actual_length = len(characters_obj) + 1

        characters_obj.extend(
            [
                {
                    'url': DOMAIN + tag.attrs["href"],
                    'parts': [number, ],
                    'id': index
                }
                for index, tag in enumerate(character_tags, start=actual_length)
            ]
        )

    # <-- Delete all duplicate pages -->
    return remove_repeat(characters_obj)


def get_stands_list() -> list:
    stands_obj = list()
    soup = fetch(f'{DOMAIN}/List_of_Stands')
    stands_tags = soup.select('div.diamond2')

    # <-- Get all characters pages -->
    for number, block in enumerate(stands_tags[:MAX_PARTS - 2], start=3):
        stands = block.select('div.charname a')
        actual_length = len(stands_obj) + 1
        stands_obj.extend(
            [
                {
                    'url': DOMAIN + tag.attrs["href"],
                    'parts': [number, ],
                    'id': index
                }
                for index, tag in enumerate(stands, start=actual_length)
            ]
        )
    # <-- Delete all duplicate pages -->

    return remove_repeat(stands_obj)


def clean_list(items_list: list) -> list:
    return sorted(items_list, key=lambda item: item.id)
