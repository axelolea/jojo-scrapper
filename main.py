from concurrent.futures import ThreadPoolExecutor
from get_list import (
    get_characters_list,
    clean_characters_list,
    get_stands_list
)
from get_data import (
    get_character_data,
    get_stand_data,
    create_files
)

def run():

    # characters_urls = get_characters_list()
    # characters = list() 
    # <-- Get info of all characters -->
    # with ThreadPoolExecutor() as executor:
    #     results = executor.map(get_character_data, characters_urls)
    # characters, errors = clean_characters_list(results)
    # create_files(characters, 'characters')
    # for item in errors:
    #     print(item)

    stands_urls = get_stands_list()
    stands = list()
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_stand_data, stands_urls)
    stands, errors = clean_characters_list(results)
    create_files(stands, 'stands')
    for item in errors:
        print(item)


# Run Main func

if __name__ == '__main__':
    run()