from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from create_driver import create_driver

from constanst import MAX_PARTS, MAX_TIME
from character import create_characters

def search_character_link(driver):
    characters_parts = dict()
    try:
        for number in range(1,MAX_PARTS + 1):
            url = f'https://jojowiki.com/Category:Part_{number}_Characters'
            driver.get(url)
            content = WebDriverWait(driver, MAX_TIME)\
                    .until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                'div.cbox'
                            )
                        )
                    )
            characters = content.find_elements(By.CSS_SELECTOR, 'div.diamond2 div.charname')
            urls = list()
            for character in characters:
                url = character.find_element(By.TAG_NAME, 'a').get_attribute('href')
                name = character.find_element(By.TAG_NAME, 'span').text
                if name:
                    urls.append(url)
                    # print(name, url, number)
            characters_parts[f'{number}'] = urls
            print(f'< Part {number} >')
    except:
        print('Algo salio mal')
    return characters_parts

if __name__ == '__main__':

    driver = create_driver()
    characters = search_character_link(driver)
    create_characters(driver, characters)
    driver.quit()