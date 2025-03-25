import re
from aiogram import types


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
