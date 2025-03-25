from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *buttons: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int, ...] = (2,),
        ):
    """
    Example for use function:
    get_keyboard(
    'Button_name_1',
    'Button_name_2',
    'Button_name_3',
    'Button_name_4',
    'Button_name_5',
    placeholder='Что Вас интересует?':
    request_contact=3,
    sizes=(2, 2, 1)
    )
    :return: keyboard
    """
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(buttons, start=0):

        if not (request_contact is None) and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif not (request_location is None) and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))

        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)


def get_list_keyboard(
        buttons: list[str],
        placeholder: str = None,
        sizes: tuple[int, ...] = (2,),
        ):
    """
    Example for use function:
    get_keyboard(
    ['Button_name_1',
    'Button_name_2',
    'Button_name_3',
    'Button_name_4',
    'Button_name_5'],
    placeholder='Что Вас интересует?':
    request_contact=3,
    sizes=(2, 2, 1)
    )
    :return: keyboard
    """
    keyboard = ReplyKeyboardBuilder()

    for text in buttons:
        keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)
