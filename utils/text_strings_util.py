from aiogram.utils import markdown


def make_string_for_output(source: tuple) -> str:
    result = (f"{markdown.hbold(source[0])}\n{markdown.hbold(source[1])}\n\n{source[2]}\n\n{markdown.hbold('Адрес: ')}"
              f"{markdown.hcode(source[3])}\n{markdown.hbold('Телефон: ')}"
              f"{markdown.hcode(make_telephone_number(source[4]))}")
    return result


def make_telephone_number(source_number: str) -> str:
    result = f"+{source_number[0]}({source_number[1:4]}){source_number[4:7]}-{source_number[7:9]}-{source_number[9:]}"
    return result


def deleting_photo_from_list(photo_list: list, photo_id: int) -> str:
    photo_list.pop(photo_id)
    result = ""
    for i in photo_list:
        result += i
        result += " "
    return result.strip()
