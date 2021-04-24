# -*- coding: utf-8 -*-

from datetime import datetime

""" This function return datetime formated for timezone pt-br """
def format_datetime(date):
    data_string = str(date)
    date = datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S.%f")
    return f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}"
    