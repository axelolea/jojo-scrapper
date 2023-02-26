from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from constanst import FOLDER_NAME, Character, Images

characters = {    
    'name': list(),
    'japanese_name': list(),
    'parts': list(),
    'alther_name': list(),
    'catchphrase': list(),
    'country': list(),
    'is_hamon_user': list(),
    'is_stand_user': list(),
    'is_gyro_user': list(),
    'living': list(),
    'is_human': list(),
    'images': list(),
    'stands': list(),
    'url': list(),
}


def get_character(driver):

    char = Character()
    # Get character info container 
    card = WebDriverWait(driver, 5)\
                .until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'aside.portable-infobox noexcerpt pi-background pi-theme-thin pi-layout-default'.replace(' ', '.')
                        )
                    )
                )
    # <-- Get Catchpharase -->
    try:
        char.catchphrase = driver.find_element(By.CSS_SELECTOR,'div#nihongo').text
    except:
        char.catchphrase = None
    # <-- Get Name -->
    char.name = card.find_element(By.CSS_SELECTOR, 'h2[data-source="title"]').text
    # <-- Get Japanese Name -->
    char.japanese_name = card.find_element(By.CSS_SELECTOR, 'div[data-source="ja_kanji"]')\
        .find_element(By.TAG_NAME, 'span').text
    # <-- Get Catchpharase -->
    try:
        items = card.find_elements(By.CSS_SELECTOR, 'div[data-source="alias"], div[data-source="namesake"]')

        alther_names:str = ', '.join([x.find_element(By.TAG_NAME, 'div').text for x in items])
        char.alther_name = alther_names

    except:
        char.alther_name = None
    # Set Stand
    try:
        char.stands = card.find_element(By.CSS_SELECTOR, 'div[data-source="stand"]')\
            .find_element(By.TAG_NAME, 'a')\
            .get_attribute('href')
        char.is_stand_user = True
    except:
        char.stand = None
        char.is_stand_user = False
    # <-- Set country -->
    try:
        char.country = card.find_element(By.CSS_SELECTOR, 'div[data-source="nation"]')\
            .find_element(By.TAG_NAME, 'img')\
            .get_attribute('alt')
    except:
        char.country = None
    # <-- Get living -->
    try:
        card.find_element(By.CSS_SELECTOR, 'div[data-source="death"]')
        char.living = False
    except:
        char.living = True

    images = Images

    # <-- Get Half Image -->
    images_container = card.find_element(By.CSS_SELECTOR, 'div[data-source="image"]')
    try:
        images_half = images_container\
            .find_elements(By.CSS_SELECTOR, '.tabber__panel')

        image_url = images_half[0].find_element(By.TAG_NAME, 'img').get_attribute('src')

        for img in images_half:
            if img.get_attribute('data-title') == 'Anime':
                image_url = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                break

        images.half_body = image_url
    except:
        # <-- Set Image -->
        images.half_body = images.find_element(By.CSS_SELECTOR, 'a.image img').get_attribute('src')
    char.images = images
    # # <-- Get Full Image -->
    # try:
    #     images = card.find_element(By.CSS_SELECTOR, 'div[data-source="image"]')\
    #         .find_element(By.CLASS_NAME, 'tabber__section')\
    #         .find_elements(By.CLASS_NAME, 'tabber__panel')
    # except:
    #     images = card.find_element(By.CSS_SELECTOR, 'div[data-source="image"]')\
    #         .find_elements(By.CSS_SELECTOR, 'a.image')

    # <-- Set part -->
    char.is_hamon_user = False
    char.is_gyro_user = False
    char.is_human = True
    return char

import json
import os

def create_csv(obj):
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    df = pd.DataFrame(obj)
    df.to_excel( FOLDER_NAME + 'character.xlsx')
    df.to_csv( FOLDER_NAME + 'character.csv')
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    with open(FOLDER_NAME + 'data.json', "w") as f:
        f.write(json.dumps(parsed, indent=2))
    print(df)


def append_obj(obj:Character):
    characters['name'].append(obj.name)
    characters['japanese_name'].append(obj.japanese_name)
    characters['parts'].append(obj.parts)
    characters['alther_name'].append(obj.alther_name)
    characters['catchphrase'].append(obj.catchphrase)
    characters['country'].append(obj.country)
    characters['is_hamon_user'].append(obj.is_hamon_user)
    characters['is_stand_user'].append(obj.is_stand_user)
    characters['is_gyro_user'].append(obj.is_gyro_user)
    characters['living'].append(obj.living)
    characters['is_human'].append(obj.is_human)
    characters['images'].append(obj.images)
    characters['stands'].append(obj.stand)
    characters['url'].append(obj.url)


def create_characters(driver, urls):
    error_urls = list()
    for number, list_urls in urls.items():
        number = 1
        for url in list_urls:
            driver.get(url)
            try:
                char = get_character(driver)
                char.parts = number
                char.url = url
                append_obj(char)
                if number >= 3:
                    break
                number = number + 1
            except:
                error_urls.append(url)
                print('<-- Error -->')
                continue
    create_csv(characters)
    if len(error_urls):
        print('<-- Urls con errores -->')
        for url in error_urls:
            print(f'<-- {url} -->')

# from create_driver import create_driver
# from time import sleep
# if __name__ == '__main__':
#     error_url = 'https://jojowiki.com/Dire'
#     number = 1
#     try:
#         driver = create_driver()
#         driver.get(error_url)
#         sleep(5)
#         try:
#             char = get_character(driver)
#         except:
#             print('salio mal')
#     except:
#         print('<-- salio algo mal -->')
#         print(f'<-- {error_url} -->')