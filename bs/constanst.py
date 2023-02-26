FOLDER_NAME = './files/bs/'

# <-- Time Values -->

MAX_TIME = 10


# <-- Search Values -->
MAX_PARTS = 2
DOMAIN = 'https://jojowiki.com'


# <-- Class -->

class Images:
    full_body:str
    half_body:str

class Character:
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
    def __init__(self) -> None:
        self.images = Images()
    def __repr__(self) -> str:
        return f'<< {self.name} / {self.url} >>'