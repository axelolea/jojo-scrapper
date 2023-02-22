from bs4 import BeautifulSoup
import requests
import pandas as pd


url_base = 'https://jojowiki.com/'
url = url_base + 'Category:Part_1_Characters'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# for character in soup.find_all('div', class_='charbox diamond resizeImg'):
#     anchor = character.a
#     span = character.span
#     print(anchor.get('href'))
#     print(span.text)

table = soup.find_all('div', class_='diamond2')
print(len(table))