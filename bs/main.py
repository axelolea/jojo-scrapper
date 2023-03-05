from constanst import DOMAIN, MAX_PARTS, MOSAIC_CHARACTERS
from concurrent.futures import ThreadPoolExecutor

characters = list()
error_characters = list()

from get_data import fetch, get_character_data, create_files

def run():

    characters_obj = list()
    # <-- Get all characters pages -->
    for number, page in enumerate(MOSAIC_CHARACTERS, start=1):
        soup = fetch(page)
        character_tags = soup.select_one('div.diamond2')\
                            .select('div.charname a')
        actual_length = len(characters_obj) + 1
        characters_obj.extend(
            [
                {
                    'page': DOMAIN + tag.attrs["href"],
                    'parts': [number,],
                    'id': index
                } 
                for index, tag in enumerate(
                    character_tags,
                    start = actual_length
                )
            ]
        )

    # <-- Delete all duplicate pages -->

    duplicated_pages = set()

    for index, item in enumerate(characters_obj):
        if index in duplicated_pages:
            continue
        comp_list = characters_obj[index + 1: len(characters_obj)]
        # Create comparative list 
        for comp_index, comp in enumerate(comp_list, start=index + 1):
            if item['page'] == comp['page']:
                characters_obj[index]['parts'].extend(characters_obj[comp_index]['parts'])
                duplicated_pages.add(comp_index)
    characters_obj = [item for index, item in enumerate(characters_obj) if index not in duplicated_pages]

    # <-- Get info of all characters -->

    with ThreadPoolExecutor() as executor:
        results = executor.map(get_character_data, characters_obj)
    for item in results:
        print(item)
    # create_files(sorted(characters, key=lambda x : x.id))
    
    # for page in error_characters:
    #     print(f'<< Error: {page} >>')

# Run Main func

if __name__ == '__main__':
    run()