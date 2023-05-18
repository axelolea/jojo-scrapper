class Images:
    # <-- Values -->
    full_body: str
    half_body: str

    def __repr__(self) -> str:
        if self.full_body and self.half_body:
            return f'<< Half / Full Body >>'
        elif self.half_body:
            return f'<< Half Body >>'
        return f'<< None >>'

    def validated(self):
        return not self.full_body or self.half_body


class BasicData:
    id: int
    name: str
    japanese_name: str
    parts: str
    alter_name: str
    images: Images
    url: str
    last_update: float

    def __init__(self, **kwargs):
        if kwargs.get('images'):
            self.images = Images()
        self.__dict__.update(**kwargs)


class Stats:
    # <-- Values -->
    power: str
    speed: str
    range: str
    durability: str
    precision: str
    potential: str

    def __repr__(self) -> str:
        return f'<< {self.power}/{self.speed}/{self.range}/' \
               f'{self.durability}/{self.precision}/{self.potential} >>'

    def validated(self) -> bool:
        values = ('NULL', 'A', 'B', 'C', 'D', 'E', 'INFINITE', '?')
        return (
                self.power in values and
                self.speed in values and
                self.range in values and
                self.durability in values and
                self.precision in values and
                self.potential in values
        )


class Character(BasicData):
    # <-- Values -->

    catchphrase: str
    country: str
    is_ripple_user: bool
    is_stand_user: bool
    is_spin_user: bool
    living: bool
    is_human: bool
    stands: list

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f'Character(<< Name <str> at {self.name}, Url <str> at {self.url}>>)'

    def validated(self):
        return (
                isinstance(self.name, str) and
                isinstance(self.japanese_name, str) and
                isinstance(self.parts, list) and
                isinstance(self.url, str) and
                self.images.validated()
        )


class Stand(BasicData):
    # <-- Values -->
    alter_name: str
    abilities: str
    battle_cry: str
    stats: Stats

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stats = Stats()

    def __repr__(self) -> str:
        return f'Stand(<< Name <str> {self.name}, Url at {self.url} >>)'

    def validated(self):
        return (
                isinstance(self.name, str) and
                isinstance(self.japanese_name, str) and
                isinstance(self.parts, list) and
                isinstance(self.abilities, str) and
                isinstance(self.url, str) and
                self.images.validated() and
                self.stats.validated()
        )
