# -*- coding: utf-8 -*-

import os
import string
import random
from datetime import datetime
from unicodedata import normalize

""" This function return datetime formated for timezone pt-br """
def format_datetime(date):
    data_string = str(date)
    date = datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S.%f")
    return f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}"

""" This function generate aleatory secret key  """
def generate_secret_key():
    key = os.urandom(2** + 10)
    return key

""" This function format text for ascci """
def format_text_for_ascci(text):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').replace(" ", "_")

""" This function genetare aleatory recovery code """
def generate_recovery_code():
    letters = string.ascii_lowercase
    code = ''.join(random.choice(letters) for i in range(5))
    return code
    