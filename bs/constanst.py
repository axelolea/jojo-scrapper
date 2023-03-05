from os import cpu_count
FOLDER_NAME = './files/bs/'

# <-- Time Values -->

MAX_TIME = 10


# <-- Search Values -->
MAX_PARTS = 1
DOMAIN = 'https://jojowiki.com'

RIPPLE_LINK = DOMAIN + '/Category:Ripple_Users'
SPIN_LINK = DOMAIN + '/Category:Spin_Users'

N_THREADS = 10
N_PROCESSES = cpu_count()

# <-- Class -->

class Images:
    full_body:str
    half_body:str
    def __repr__(self) -> str:
        if self.full_body and self.half_body :
            return f'<< Half Body / Full Body >>'
        elif self.half_body:
            return f'<< Half Body >>'
        else:
            return f'<< None >>'

class Character:
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
    def __init__(self) -> None:
        self.images = Images()
    def __repr__(self) -> str:
        return f'Character(<<Name <str> at {self.name}, Url <str> at {self.url}>>)'