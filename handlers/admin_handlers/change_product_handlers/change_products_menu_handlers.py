from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule
from keyboards import (cancel_keyboard, admin_change_products_menu, build_change_record_kb,
                       build_delete_photo_record_kb, admin_change_category_products)
from config import moto_db, ADMIN_ID
from utils import make_string_for_output

router = Router()


#  Not ready to test
@router.message(AdminToolsModule.change_products_menu, F.text.casefold() == "изменить товар 📄")
async def changing_product_handler(message: types.Message, state: FSMContext):
    list_of_places = []
    try:
        async with moto_db:
            list_of_places = await moto_db.get_our_places()
    except Exception as ex:
        await message.answer(text="Не могу подключиться к базе данных. Попробуйте позже.")
        print(f"Exception: {ex}")

    #  Output all places from list_of_places
    for i in list_of_places:
        data_tuple = (i[1], i[3], i[2], i[4], i[5], i[7])
        string_for_output = make_string_for_output(data_tuple)
        user_id = message.from_user.id
        keyboard = build_change_record_kb(place_id=i[0], user_id=user_id, reaction="change place")
        if i[7]:
            await message.answer_photo(photo=i[7].split()[0], caption=string_for_output, reply_markup=keyboard)
            await state.update_data(has_photo=True)
        else:
            await message.answer(text=string_for_output, reply_markup=keyboard)
            await state.update_data(has_photo=False)
    #  print(f"our places: {list_of_places}")
    keyboard = get_keyboard("Отмена 🔙",
                            placeholder="Введите название",
                            sizes=(1,))
    await state.set_state(AdminToolsModule.start_change_place)
    await message.answer(
        text="Выберите площадку, информацию о которой Вы хотите изменить ☝️.",
        reply_markup=keyboard
    )


#  Ready to test
@router.message(AdminToolsModule.change_products_menu, F.text.casefold() == "добавить товар ➕")
async def adding_product_handler(message: types.Message, state: FSMContext):
    keyboard = get_keyboard("Отмена 🔙",
                            placeholder="Введите название",
                            sizes=(1,))
    await state.update_data(step=[AdminToolsModule.change_products_menu])
    await state.set_state(AdminToolsModule.adding_products)
    await message.answer(
        text="Вы перешли в добавление нового товара.\nВведите название товара:",
        reply_markup=keyboard
    )


#  Not ready to test
@router.message(AdminToolsModule.change_products_menu, F.text.casefold() == "удалить промо ❌")
async def deleting_product_handler(message: types.Message, state: FSMContext):
    keyboard = cancel_keyboard
    await state.set_state(AdminToolsModule.deleting_place)
    await state.update_data(step=[AdminToolsModule.deleting_place])
    try:
        async with moto_db:
            places = await moto_db.get_our_places()
            text = "Выберите площадку для удаления из базы данных ☝️."
    except Exception as ex:
        print(f"Exception:\n{ex}")
        text = "Возникла ошибка при подключении к базе данных. Попробуйте позднее."

    if places:
        for element in places:
            text_for_send = make_string_for_output(element[1:6])
            if element[-1]:
                await message.answer_photo(photo=element[-1].split()[0],
                                           caption=text_for_send,
                                           reply_markup=build_delete_photo_record_kb(
                                                                                    place_id=element[0],
                                                                                    photo_id=0,
                                                                                    reaction="delete place",
                                                                                    text="Удалить площадку"))
            else:
                await message.answer(text=text_for_send, reply_markup=build_delete_photo_record_kb(
                                                                                    place_id=element[0],
                                                                                    photo_id=0,
                                                                                    reaction="delete place",
                                                                                    text="Удалить площадку"))
    else:
        text = "Отсутствуют площадки для удаления.\nВыберите действие."
    await message.answer(
        text=text,
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.change_products_menu, F.text.casefold() == "изменить категории товаров",
                F.from_user.id.in_(ADMIN_ID))
async def change_contacts_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_category_menu)
    keyboard = admin_change_category_products
    await message.answer(
        text="Вы перешли в меню изменения категорий товаров. Выберите действие 👇:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.change_products_menu)
async def wrong_menu_product_change_handler(message: types.Message):
    keyboard = admin_change_products_menu
    await message.answer(
        text="Я Вас не понимаю.\nВыберите пункт меню 👇:",
        reply_markup=keyboard
    )
