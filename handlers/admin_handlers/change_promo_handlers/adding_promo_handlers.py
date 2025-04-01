from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from keyboards import cancel_keyboard, action_with_record_ikb
from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule

from config import moto_db
from utils import make_string_for_output

router = Router()


@router.message(AdminToolsModule.adding_promo, F.text)
async def adding_promo_title_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_promo_description)
    current_data = await state.get_data()
    current_promo_list = current_data["promo_list"]
    current_buttons_set = current_data["buttons_set"]
    promo_title_index = 0
    if message.text in current_buttons_set:
        for i in current_promo_list:
            if i[1] == message.text:
                promo_title_index = i[0]
        if promo_title_index != 0:
            await state.update_data(promo_title_name=message.text, promo_title_index=promo_title_index)
            text = f"Название акции: {markdown.hbold(message.text)} выбрано.\nВведите описание акции:"
        else:
            text = f"Не удалось найти индекс акции: {message.text}"
    else:
        promo_title_name = message.text
        try:
            async with moto_db:
                saved_id = await moto_db.save_new_promo_title(promo_title_name)
                print(f"saved_id = {saved_id}")
                if saved_id:
                    await state.update_data(promo_title_name=promo_title_name, promo_title_index=saved_id[0])
                    text = f"Название акции: {markdown.hbold(message.text)} внесено в базу.\nВведите описание акции:"
                else:
                    text = "Не удалось записать название промо-акции в базу. Попробуйте позже."
        except Exception as ex:
            print(f"Ошибка при записи названия промо-акции {ex}")
            text = "Не удалось записать название промо-акции в базу. Попробуйте позже."

    await message.answer(text=text)


@router.message(AdminToolsModule.adding_promo, F.text)
async def wrong_adding_promo_title_handler(message: types.Message, state: FSMContext):
    keyboard = ...
    await message.answer(text="Я Вас не понимаю. Выберите название акции или введите вручную.",
                         reply_markup=keyboard)
