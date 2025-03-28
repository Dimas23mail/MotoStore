from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule

router = Router()


@router.message(Command("back"))
@router.message(F.text.casefold() == "назад")
@router.message(F.text.casefold() == "назад 🔙")
@router.message(F.text.casefold() == "back")
async def back_adding_place_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    current_step_list = current_data["step"]
    caption = ""
    text = "не попал в state"
    button_name = "Отмена 🔙"
    current_step = current_step_list.pop()
    if current_step in (AdminToolsModule.input_place_name,):
        caption = "Введите название площадки:"
        text = "Вы отменили ввод. Введите название площадки:"
    elif current_step in (AdminToolsModule.input_place_description,):
        caption = "Введите краткое описание площадки:"
        text = "Вы отменили ввод. Введите краткое описание площадки:"
        button_name = "Назад 🔙"
    elif current_step in (AdminToolsModule.input_place_city,):
        caption = "Введите название города:"
        text = "Вы отменили ввод. Введите название города:"
        button_name = "Назад 🔙"
    elif current_step in (AdminToolsModule.input_place_address,):
        caption = "Введите адрес:"
        text = "Вы отменили ввод. Введите адрес:"
        button_name = "Назад 🔙"
    elif current_step in (AdminToolsModule.input_place_telephone,):
        caption = "Введите телефон:"
        text = "Вы отменили ввод. Введите телефон:"
        button_name = "Назад 🔙"

    await state.set_state(current_step)
    keyboard = get_keyboard(button_name,
                            placeholder=caption,
                            sizes=(1,))
    await message.answer(text=text, reply_markup=keyboard)
