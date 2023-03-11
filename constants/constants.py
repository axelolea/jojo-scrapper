from bs4 import BeautifulSoup
from requests import Session

session = Session()


# <-- Functions -->
def fetch(url: str) -> BeautifulSoup:
    resp = session.get(url)
    content = resp.content
    return BeautifulSoup(content, 'html.parser')


# <-- Directory values -->
FOLDER_NAME = './files/'

# <-- Search Values -->
MAX_PARTS = 1
DOMAIN = 'https://jojowiki.com'

