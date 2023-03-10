from concurrent.futures import ThreadPoolExecutor
from get_list import (
    get_characters_list,
    clean_list,
    get_stands_list
)
from get_data_characters import (
    get_character_data,
    get_stand_data,
    create_files
)


def main() -> None:
    # <-- Scrap Characters Data --> 
    # run(get_characters_list(), get_character_data, 'characters')
    # <-- Scrap Stands Data -->
    run(get_stands_list(), get_stand_data, 'stands')


def run(urls: list, data_func, filename: str) -> None:

    with ThreadPoolExecutor() as executor:
        results = executor.map(data_func, urls)
    # items = clean_list(results)
    create_files(results, filename)


# Run Main func
if __name__ == '__main__':
    main()
