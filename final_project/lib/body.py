import datetime
import sqlite3
from .error_codes import *
from .fitbook_db import *

MAX_BODY_WEIGHT = 1000
MAX_MUSCLE_WEIGHT = 1000
MAX_FAT_RATE = 100


def is_body_weight_valid(body_weight):
    try:
        body_weight = float(body_weight)
    except Exception as e:
        print(e)
        return False
    if 0 < body_weight < MAX_BODY_WEIGHT:
        return True
    else:
        return False


def is_muscle_weight_valid(muscle_weight):
    try:
        muscle_weight = float(muscle_weight)
    except Exception as e:
        print(e)
        return False
    if 0 < muscle_weight < MAX_MUSCLE_WEIGHT:
        return True
    else:
        return False


def is_fat_rate_valid(fat_rate):
    try:
        fat_rate = float(fat_rate)
    except Exception as e:
        print(e)
        return False
    if 0 < fat_rate < MAX_FAT_RATE:
        return True
    else:
        return False