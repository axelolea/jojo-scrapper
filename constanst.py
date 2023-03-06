from bs4 import BeautifulSoup
from requests import Session

session = Session()

# <-- Funcionts -->

def fetch(url:str) -> BeautifulSoup:
    resp = session.get(url)
    content = resp.content
    return BeautifulSoup(content, 'html.parser')

# <-- Directory values -->

FOLDER_NAME = './files/'

# <-- Search Values -->

MAX_PARTS = 9
DOMAIN = 'https://jojowiki.com'

STATS_VALUES = ('NULL', 'A', 'B', 'C', 'D', 'E', 'INFINITE', '?')

# <-- Class -->

class Images:

    # <-- Values -->
    full_body:str
    half_body:str

    def __repr__(self) -> str:
        if self.full_body and self.half_body :
            return f'<< Half Body / Full Body >>'
        elif self.half_body:
            return f'<< Half Body >>'
        else:
            return f'<< None >>'


class Stats():

    # <-- Values -->
    power:str
    speed:str
    range:str
    durability:str
    precision:str
    potential:str
    def __repr__(self) -> str:
        return f'<< {self.power}/{self.speed}/{self.range}/{self.durability}/{self.precision}/{self.potential} >>'

class Character:

    # <-- Values -->

    id:int
    name:str
    japanese_name:str
    parts:str
    alther_name:str
    catchphrase:str
    country:str
    is_hamon_user:bool
    is_stand_user:bool
    is_gyro_user:bool
    living:bool
    is_human:bool
    images:Images
    stands:list
    url:str
    # def __init__(self) -> None:
    #     self.images = Images()
    def __repr__(self) -> str:
        return f'Character(<<Name <str> at {self.name}, Url <str> at {self.url}>>)'
    
class Stand():
    # <-- Values -->
    id:int
    name:str
    japanese_name:str
    parts:list
    alther_name:str
    abilities:str
    battlecry:str
    images:Images
    stats:Stats
    url:str
    # def __init__(self) -> None:
    #     self.images = Images()
    #     self.stats = Stats()
    def __repr__(self) -> str:
        return f'Stand(<< Name <str> {self.name}, Url at {self.url} >>)'