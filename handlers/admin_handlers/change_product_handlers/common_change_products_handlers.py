from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.reply_keyboard import get_keyboard, get_list_keyboard
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
    keyboard = None
    if current_step in (AdminToolsModule.adding_promo,):
        text = "Вы отменили ввод. Введите название промо-акции:"
        current_buttons_set = current_data["buttons_set"]
        current_buttons_set = list(current_buttons_set)
        current_buttons_set.append("Отмена 🔙")
        keyboard = get_list_keyboard(buttons=current_buttons_set, placeholder="Выберите название или введите вручную",
                                     sizes=(2,))

    elif current_step in (AdminToolsModule.adding_promo_description,):
        caption = "Введите краткое описание промо-акции:"
        text = "Вы отменили ввод. Введите краткое описание промо-акции:"
        button_name = "Назад 🔙"

    elif current_step in (AdminToolsModule.adding_promo_discount,):
        caption = "Введите скидку по акции (со знаком %):"
        text = "Вы отменили ввод. Введите скидку по акции (со знаком %):"
        button_name = "Назад 🔙"

    elif current_step in (AdminToolsModule.adding_promo_start_date,):
        text = "Вы отменили ввод. Введите дату начала акции:"
        button_name = "Назад 🔙"
        keyboard = get_keyboard("Назад 🔙",
                                "Пропустить",
                                placeholder="Введите дату (dd.mm.yyyy)")

    elif current_step in (AdminToolsModule.adding_promo_end_date,):
        caption = "Введите дату (dd.mm.yyyy)"
        text = "Вы отменили ввод. Введите дату окончания акции:"
        button_name = "Назад 🔙"

    # ----------------------------------

    await state.set_state(current_step)
    if keyboard is None:
        keyboard = get_keyboard(button_name, placeholder=caption, sizes=(1,))
    await message.answer(text=text, reply_markup=keyboard)
