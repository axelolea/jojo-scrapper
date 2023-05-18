from bs4 import BeautifulSoup
from requests import Session
from functools import lru_cache


# <-- Functions -->
class Scrapper:
    session: Session

    def __init__(self):
        self.session = Session()

    def fetch(self, url: str) -> BeautifulSoup:
        resp = self.session.get(url)
        content = resp.content
        return BeautifulSoup(content, 'html.parser')


@lru_cache()
def get_scrapper() -> Scrapper:
    return Scrapper()
