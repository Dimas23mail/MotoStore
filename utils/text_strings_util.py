from aiogram.utils import markdown


#  String for contact list
def make_string_for_output(source: tuple) -> str:
    result = (f"{markdown.hbold(source[0])}\n\nг. {markdown.hbold(source[1])}\n\n{markdown.hbold('Адрес: ')}"
              f"{markdown.hcode(source[2])}\n{markdown.hbold('Телефон: ')}"
              f"{markdown.hcode(make_telephone_number(source[3]))}")
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


#  String for promo list (title, description, start_date, end_date)
def make_promo_string(source: tuple) -> str:
    result = (f"{markdown.hbold(source[0])}\n{source[1]}\n\n"
              f"Начало акции: {markdown.code(make_date_time_string(source[2]))},\n"
              f"Окончание акции: {markdown.code(make_date_time_string(source[3]))}!")

    return result


def make_date_time_string(source_string: str) -> str:
    result = source_string[:source_string.find(" ")] + " в " + source_string[source_string.find(" ")+1:]
    return result
