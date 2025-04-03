import asyncio
import datetime
import re
from calendar import monthrange

from aiogram import types
from aiogram.fsm.context import FSMContext


def telephone_validate(number: types.Message) -> str | None:
    number_from_text = ""
    for i in number.text:
        if i.isdigit():
            number_from_text += i
    if len(number_from_text) != 10 and len(number_from_text) != 11 and len(number_from_text) != 6:
        return None
    if len(number_from_text) == 10:
        number_from_text = "7" + number_from_text
    pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    result = re.match(pattern=pattern, string=number_from_text)[0]
    if result:
        return result
    else:
        return None


def discount_validate(discount: types.Message) -> float | None:
    result_discount = ''
    if discount.text.isdigit():
        result_discount = float(discount.text)
    else:
        pattern = r'\d{,2}[%.,]\d{,2}'
        list_in_first = re.match(pattern=pattern, string=discount.text)
        count_dot = 0
        for i in list_in_first[0]:
            if i.isdigit():
                result_discount += i
            elif (i == "," or ".") and count_dot == 0:
                count_dot += 1
                result_discount += "."
            elif ((i == "," or ".") and count_dot > 0) or i == "%":
                break
    if result_discount:
        result_discount = float(result_discount)
        return result_discount
    else:
        return None


def date_validate(message_date: types.Message) -> str | None:
    pattern_1 = r'\d{,2}[-./]\d{,2}[-./]\d{,4}'
    result_date = ""
    dot_count = 0
    first_res = re.match(pattern=pattern_1, string=message_date.text)[0]
    for i in first_res:
        if i.isdigit():
            result_date += i
        elif (i == "/" or i == "." or i == "-") and dot_count < 2:
            result_date += "."
        elif dot_count >= 2:
            break
    data_list = result_date.split(".")
    if len(data_list) < 3 or int(data_list[1]) <= 0 or int(data_list[1]) > 12:
        return None
    if len(data_list[2]) == 2:
        data_list[2] = "20" + data_list[2]
    if datetime.datetime(int(data_list[2]), int(data_list[1]), int(data_list[0])).year:
        source_year = datetime.datetime(int(data_list[2]), int(data_list[1]), int(data_list[0])).year
    else:
        return None
    month_days = monthrange(source_year, int(data_list[1]))[1]
    if int(data_list[0]) <= 0 or int(data_list[0]) > month_days:
        return None
    result = data_list[0] + "." + data_list[1] + "." + data_list[2]
    return result


def days_validate(message_days: types.Message) -> int | None:
    return int(message_days.text) if message_days.text.isdigit() else None
