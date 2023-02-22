from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def create_driver():
    binary_location = '/usr/bin/google-chrome'
    rute = ChromeDriverManager(path='./driver').install()
    service = Service(rute)
    options = Options()
    user_agent = ''
    options.binary_location = binary_location
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--no-proxy-server')
    options.add_argument('--disable-blink-features=AutomationControlled')
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]
    options.add_experimental_option('excludeSwitches', exp_opt)
    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        'intl.accept_languages': ['es-ES', 'es'],
        'credentials_enable_service': False
    }
    options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(service=service, options=options)


if __name__ == '__main__':
    urls = ['https://jojowiki.com/Jonathan_Joestar',
            'https://jojowiki.com/Jonathan_Joestar',
            'https://jojowiki.com/Jotaro_Kujo',
            'https://jojowiki.com/Josuke_Higashikata',
            'https://jojowiki.com/Giorno_Giovanna',
            'https://jojowiki.com/Jolyne_Cujoh',
            'https://jojowiki.com/Josuke_Higashikata_(JoJolion)',
            'https://jojowiki.com/Jodio_Joestar'
            ]
    url = 'https://jojowiki.com/Jonathan_Joestar'
    # url = 'https://jojowiki.com/Johnny_Joestar'
    driver = create_driver()
    driver.get(url)
    try:

        catchphrase = WebDriverWait(driver, 5)\
            .until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'div#nihongo'
                    )
                )
            )
        
        card = WebDriverWait(driver, 5)\
            .until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'aside.portable-infobox noexcerpt pi-background pi-theme-thin pi-layout-default'.replace(' ', '.')
                    )
                )
            )

        name = card.find_element(By.CSS_SELECTOR, 'h2[data-source="title"]')
        japanese_name = card.find_element(By.CSS_SELECTOR, 'div[data-source="ja_kanji"]')\
            .find_element(By.TAG_NAME, 'span')
        alther_name = card.find_element(By.CSS_SELECTOR, 'div[data-source="alias"]')\
            .find_element(By.TAG_NAME, 'div')
        stand = card.find_element(By.CSS_SELECTOR, 'div[data-source="stand"]')\
            .find_element(By.TAG_NAME, 'a')
        country = card.find_element(By.CSS_SELECTOR, 'div[data-source="nation"]')\
            .find_element(By.TAG_NAME, 'img')

        # images = card.find_element(By.CSS_SELECTOR, 'div[data-source="image"]')\
        #     .find_element(By.CLASS_NAME, 'tabber__tabs')\
        #     .find_elements(By.CLASS_NAME, 'tabber__tab')
        images = card.find_element(By.CSS_SELECTOR, 'div[data-source="image"]')\
            .find_element(By.CLASS_NAME, 'tabber__section')\
            .find_elements(By.CLASS_NAME, 'tabber__panel')

        image = card.find_element(By.CSS_SELECTOR, 'div[data-source="image"]')\
            .find_element(By.TAG_NAME, 'img')

        for tab in images:
            if tab.get_attribute('data-title') == 'Anime':
                image = tab.find_element(By.TAG_NAME, 'img')
                print(image)
                break

        print(name.text)
        print(japanese_name.text)
        print(alther_name.text)
        print(catchphrase.text.split(' (')[0])
        print(stand.text)
        print(country.get_attribute('alt'))
        print(image.get_attribute('src'))
        
    except:
        driver.quit()
    driver.quit()
