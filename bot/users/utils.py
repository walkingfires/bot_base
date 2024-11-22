import calendar
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from bot.config import constants


def calendar_flipper(date_data: date, backward: bool = True):
    if backward:
        return date_data - relativedelta(months=1)
    else:
        return date_data + relativedelta(months=1)


def get_month_info(date_data: date):
    year = date_data.year
    month = date_data.month

    return {
        "year": year,
        "month": month,
        # "month_name_en": calendar.month_name[month],
        "month_name_ru": constants.RUSSIAN_MONTHS[month - 1],
        "num_days": calendar.monthrange(year, month)[1]
    }


def pack_date(date_data: date):
    return date_data.strftime("%Y-%m-%d")


# Function to unpack a string back into a datetime object
def unpack_date(date_data: date):
    return datetime.strptime(date_data, "%Y-%m-%d").date()
