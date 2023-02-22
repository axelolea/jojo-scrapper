from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

import time

TIMELAPS = 2

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

time.sleep(TIMELAPS)


names = list()
links = list()
parts = list()
def search_character_link():
    for number in range(1,9):
        url = f'https://jojowiki.com/Category:Part_{number}_Characters'
        driver.get(url)
        time.sleep(TIMELAPS)
        content = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/div[16]/div/div[2]')
        characters = content.find_elements(By.CSS_SELECTOR, '.charbox.diamond.resizeImg')

        for character in characters:
            name = character.find_element(By.CLASS_NAME, 'charwhitelink').text
            url = character.find_element(By.XPATH, './/div[2]/a').get_attribute('href')
            if name:
                names.append(name)
                links.append(url)
                parts.append(number)
                print(name, url)

search_character_link()

df = pd.DataFrame({'name': names, 'link': links})
print(df)
df.to_csv('./data.csv')
time.sleep(1)

driver.quit()