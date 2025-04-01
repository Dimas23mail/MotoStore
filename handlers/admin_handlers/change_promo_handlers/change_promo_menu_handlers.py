from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from keyboards import cancel_keyboard, action_with_record_ikb
from keyboards.reply_keyboard import get_keyboard, get_list_keyboard
from storage import AdminToolsModule

from config import moto_db
from utils import make_string_for_output

router = Router()


@router.message(AdminToolsModule.change_promo_menu, F.text.casefold() == "добавить промо-акцию ➕")
async def adding_promo_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_promo)
    try:
        async with moto_db:
            promo_list = await moto_db.get_all_promo()
    except Exception as ex:
        print(f"Ошибка при чтении из промо-акций: {ex}")
    await state.update_data(promo_list=promo_list)
    if promo_list:
        buttons = set()
        for i in promo_list:
            buttons.add(i[1])
        await state.update_data(buttons_set=buttons)
        buttons = list(buttons)
        text = "Вы перешли в меню добавления промо-акции.\nВыберите название акции или введите новое 👇."
        keyboard = get_list_keyboard(buttons=buttons, placeholder="Выберите или введите название", sizes=(2, ))
    else:
        text = "Названия промо-акций в базе отсутствуют 😕.\nВведите название новой промо-акции."
        keyboard = cancel_keyboard
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.change_promo_menu, F.text.casefold() == "удалить промо-акцию ❌")
async def deleting_promo_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.deleting_promo)
    #  Запрос всех акций + кнопка удаления
    try:
        async with moto_db:
            contacts_list = await moto_db.get_all_contacts()
            if contacts_list:
                for element in contacts_list:
                    text = make_string_for_output(source=element[1:])
                    #  keyboard = action_with_record_ikb(record_id=element[0], reaction="delete contact")
                    #  await message.answer(text=text, reply_markup=keyboard)
                text = "Вы перешли в меню удаления промо-акций. Выберите данные для удаления ☝️:"
            else:
                text = "В базе данных отсутствуют промо-акции."
    except Exception as ex:
        print(f"Exception in delete promo: {ex}")

    keyboard = get_keyboard("Завершить",
                            placeholder="Выберите действие",
                            sizes=(1,))
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.change_promo_menu, F.text.casefold() == "проверить промо-код 🧑‍💻")
async def testing_promo_menu_handler(message: types.Message, state: FSMContext):
    #  Запрос промо-кода и проверка его в БД + срок действия
    await state.set_state(AdminToolsModule.testing_promo_code)
    await state.update_data(step=[AdminToolsModule.change_contact_menu,])
    await message.answer(text="Вы перешли в меню проверки промо-кода.\nВведите промо-код.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.change_promo_menu)
async def wrong_adding_promo_menu_handler(message: types.Message):
    await message.answer(text="Я Вас не понимаю.\nВыберите действие.",
                         reply_markup=cancel_keyboard)
