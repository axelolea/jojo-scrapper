FOLDER_NAME = './files/se/'

MAX_TIME = 10
MAX_PARTS = 2

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
    def __repr__(self) -> str:
        return f'< {self.name} - {self.url} >'