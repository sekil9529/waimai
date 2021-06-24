# coding: utf-8

import datetime


def get_date_1th_of_current_month():
    """本月一号"""
    today = datetime.date.today()
    date_1th = today.replace(day=1)
    return date_1th
