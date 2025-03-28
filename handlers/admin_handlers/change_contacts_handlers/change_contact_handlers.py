from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import admin_change_contact, admin_finish_action
from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule
from user_filters import telephone_validate
from config import moto_db
from utils import make_string_for_output, StorageForChangingContacts

router = Router()


@router.callback_query(StorageForChangingContacts.filter(F.reaction == "change contact"))
async def deleting_contact_reaction(callback: CallbackQuery, callback_data: StorageForChangingContacts,
                                    state: FSMContext) -> None:
    await callback.answer(text=f"Изменяем контакт.",
                          show_alert=False)
    await callback.message.edit_text(text="Контакт в статусе изменения...", reply_markup=None)

    contact_id = callback_data.contact_id
    await state.update_data(contact_id=contact_id)
    try:
        async with moto_db:
            contact_tuple = await moto_db.get_one_contact(contact_id=contact_id)
            text_from_tuple = make_string_for_output(source=contact_tuple[1:])
            text = f"Для изменения Вы выбрали контакт:\n{text_from_tuple}\n\nКакие сведения Вы хотите изменить?👇:"
            keyboard = admin_change_contact
    except Exception as ex:
        print(f"Exception:\n{ex}")
        text = "Возникла ошибка при подключении к базе данных. Попробуйте позднее."
        keyboard = get_keyboard("Завершить",
                                placeholder="Выберите действие",
                                sizes=(1,))
    await callback.message.answer(text=text,
                                  reply_markup=keyboard)


@router.message(AdminToolsModule.change_contact_main, F.text.casefold() == "название 🪧")
async def start_changing_title_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_title)
    await message.answer(text="Введите новое название контакта:", reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_main, F.text.casefold() == "город 🏙")
async def start_changing_city_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_city)
    await message.answer(text="Введите новый город контакта:", reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_main, F.text.casefold() == "адрес 🏘")
async def start_changing_address_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_address)
    await message.answer(text="Введите новый адрес контакта:", reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_main, F.text.casefold() == "телефон ☎️")
async def start_changing_phone_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_phone)
    await message.answer(text="Введите новый номер телефона:", reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_main)
async def wrong_changing_contact(message: types.Message) -> None:
    #  await state.set_state(AdminToolsModule.change_contact_main)
    await message.answer(text="Я Вас не понимаю! Выберите сведения для изменения:", reply_markup=admin_change_contact)


# Обработка каждой кнопки
@router.message(AdminToolsModule.change_contact_title, F.text)
async def changing_title_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_main)
    current_data = await state.get_data()
    contact_id = current_data["contact_id"]
    async with moto_db:
        try:
            async with moto_db:
                if await moto_db.update_contact(contact_id=contact_id, contact_title=message.text):
                    text = "Название контакта изменено!\nКакие сведения Вы хотите изменить?👇:"
                else:
                    text = "Неверно указан contact_id"
        except Exception as ex:
            print(f"Exception in contact title changer: {ex}")
            text = "Возникла ошибка при записи в базу данных, попробуйте позднее."
    await message.answer(text=text, reply_markup=admin_change_contact)


@router.message(AdminToolsModule.change_contact_title, F.text)
async def wrong_changing_title_contact(message: types.Message) -> None:
    await message.answer(text="Я Вас не понимаю! Введите название контакта:",
                         reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_city, F.text)
async def changing_city_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_main)
    current_data = await state.get_data()
    contact_id = current_data["contact_id"]
    async with moto_db:
        try:
            async with moto_db:
                if await moto_db.update_contact(contact_id=contact_id, contact_city=message.text):
                    text = "Город контакта изменен!\nКакие сведения Вы хотите изменить?👇:"
                else:
                    text = "Неверно указан contact_id"
        except Exception as ex:
            print(f"Exception in contact title changer: {ex}")
            text = "Возникла ошибка при записи в базу данных, попробуйте позднее."
    await message.answer(text=text, reply_markup=admin_change_contact)


@router.message(AdminToolsModule.change_contact_city, F.text)
async def wrong_changing_city_contact(message: types.Message) -> None:
    await message.answer(text="Я Вас не понимаю! Введите город контакта:",
                         reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_address, F.text)
async def changing_address_contact(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_main)
    current_data = await state.get_data()
    contact_id = current_data["contact_id"]
    async with moto_db:
        try:
            async with moto_db:
                if await moto_db.update_contact(contact_id=contact_id, contact_address=message.text):
                    text = "Адрес контакта изменен!\nКакие сведения Вы хотите изменить?👇:"
                else:
                    text = "Неверно указан contact_id"
        except Exception as ex:
            print(f"Exception in contact title changer: {ex}")
            text = "Возникла ошибка при записи в базу данных, попробуйте позднее."
    await message.answer(text=text, reply_markup=admin_change_contact)


@router.message(AdminToolsModule.change_contact_city, F.text)
async def wrong_changing_address_contact(message: types.Message) -> None:
    await message.answer(text="Я Вас не понимаю! Введите адрес контакта:",
                         reply_markup=admin_finish_action)


@router.message(AdminToolsModule.change_contact_phone, F.func(telephone_validate).as_("phone"))
async def changing_phone_contact(message: types.Message, state: FSMContext, phone: str) -> None:
    await state.set_state(AdminToolsModule.change_contact_main)
    current_data = await state.get_data()
    contact_id = current_data["contact_id"]
    async with moto_db:
        try:
            async with moto_db:
                if await moto_db.update_contact(contact_id=contact_id, contact_phone=phone):
                    text = "Телефон контакта изменен!\nКакие сведения Вы хотите изменить?👇:"
                else:
                    text = "Неверно указан contact_id"
        except Exception as ex:
            print(f"Exception in contact title changer: {ex}")
            text = "Возникла ошибка при записи в базу данных, попробуйте позднее."
    await message.answer(text=text, reply_markup=admin_change_contact)


@router.message(AdminToolsModule.change_contact_phone)
async def wrong_changing_phone_contact(message: types.Message) -> None:
    await message.answer(text="Я Вас не понимаю! Введите телефон контакта:",
                         reply_markup=admin_finish_action)
