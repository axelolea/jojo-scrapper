from math import ceil, sqrt
from functools import lru_cache
from constants.constants import MONTHS
from re import search, sub
import datetime


def get_date(date_str: str) -> datetime.datetime:
    # Date Day/Month(str)/year"  (10 May 2023)
    date_string = search(r'\d{1,2}\s[a-zA-Z]+\s\d{4}', date_str).group().lower()
    date_month = search(r'[a-z]+', date_string).group()
    new_date_string = sub(date_month, MONTHS[date_month], date_string)
    return datetime.datetime.strptime(new_date_string, '%d %m %Y')


def get_last_update(date_str: str) -> float:
    last_date = get_date(date_str)
    return last_date.timestamp()


@lru_cache()
def get_image_select(n_images: int) -> int:
    square_number = sqrt(n_images)
    return ceil(square_number) - 1
