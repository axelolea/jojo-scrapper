from concurrent.futures import ThreadPoolExecutor
from get_list import (
    create_files,
    get_characters_pages,
    get_stands_pages
)

from get_data.stands import get_stand_data
from get_data.characters import get_character_data


def main() -> None:
    # <-- Scrap Characters Data --> 
    run(get_characters_pages(), get_character_data, 'characters')
    # <-- Scrap Stands Data -->
    # run(get_stands_pages(), get_stand_data, 'stands')


def run(urls: set, data_func, filename: str) -> None:
    with ThreadPoolExecutor() as executor:
        results = executor.map(data_func, urls)
    create_files(results, filename)


# Run Main func
if __name__ == '__main__':
    main()
