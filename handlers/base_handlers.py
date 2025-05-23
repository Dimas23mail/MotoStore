import asyncio
import datetime
import pytz

from aiogram.filters import CommandStart, Command
from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.utils.chat_action import ChatActionSender

from config import ADMIN_ID, moto_db
from keyboards import (start_client_reply_keyboard, start_admin_reply_keyboard, admin_main_menu,
                       admin_change_category_products)
from keyboards.admin_reply_keyboards import admin_change_contact_menu, admin_change_products_menu
from storage import AdminToolsModule, ClientToolsModule

router = Router(name=__name__)


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
@router.message(F.text.casefold() == "отмена 🔙")
@router.message(F.text.casefold() == "cancel")
@router.message(F.text.casefold() == "завершить")
async def cancel_base_handler(message: types.Message, state: FSMContext):

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await asyncio.sleep(1)

    admin_zero_level_menu_states = (AdminToolsModule.main_menu_admin,)

    changing_category_states = (AdminToolsModule.adding_category, AdminToolsModule.deleting_category)

    changing_spare_types_states = (AdminToolsModule.adding_spare_types, AdminToolsModule.deleting_spare_types)

    changing_category_menu_states = (AdminToolsModule.change_category_menu, AdminToolsModule.change_spare_types_menu)

    admin_first_menu_states = (AdminToolsModule.change_contact_menu, AdminToolsModule.change_products_menu)

    any_contacts_states = (AdminToolsModule.adding_contact_title, AdminToolsModule.adding_contact_city,
                           AdminToolsModule.adding_contact_address, AdminToolsModule.adding_contact_phone,
                           AdminToolsModule.delete_contact_main, AdminToolsModule.change_contact_main,
                           AdminToolsModule.change_contact_title, AdminToolsModule.change_contact_city,
                           AdminToolsModule.change_contact_address, AdminToolsModule.change_contact_phone)

    client_zero_states = (ClientToolsModule.main_state_client, )

    print("cancel button")
    current_state = await state.get_state()
    print(f"current state = {current_state}")
    await state.set_state(AdminToolsModule.main_state_admin)
    keyboard = start_admin_reply_keyboard
    text = "Вы вышли в главное меню. Выберите пункт меню 👇:"

    if current_state in changing_category_states:
        keyboard = admin_change_category_products
        await state.set_state(AdminToolsModule.change_category_menu)
        text = "Вы вышли в меню изменения категории товаров.\nВыберите пункт меню 👇:"
    elif current_state in changing_spare_types_states:
        await state.set_state(AdminToolsModule.change_category_menu)
        text = "Вы вышли в меню изменения видов запчастей.\nВыберите пункт меню 👇:"
    elif current_state in changing_category_menu_states:
        keyboard = admin_change_products_menu
        await state.set_state(AdminToolsModule.change_products_menu)
        text = "Вы вышли в главное меню изменения товаров.\nВыберите пункт меню 👇:"
    elif current_state in any_contacts_states:
        keyboard = admin_change_contact_menu
        await state.set_state(AdminToolsModule.change_contact_menu)
        text = "Вы вышли в меню изменения контактных данных.\nВыберите пункт меню 👇:"
    elif current_state in admin_first_menu_states:
        keyboard = admin_main_menu
        await state.set_state(AdminToolsModule.main_menu_admin)
        text = "Вы вышли в главное меню изменения контактных данных.\nВыберите пункт меню 👇:"
    elif current_state in admin_zero_level_menu_states:
        keyboard = start_admin_reply_keyboard
        await state.set_state(AdminToolsModule.main_state_admin)
        text = "Вы вышли в главное меню.\nВыберите пункт меню 👇:"

    #  For client states
    elif current_state in client_zero_states:
        keyboard = start_client_reply_keyboard
        await state.set_state(ClientToolsModule.main_state_client)
        text = "Вы вышли в главное меню.\nВыберите пункт меню 👇:"

    await message.answer(text=text,
                         reply_markup=keyboard)


@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    print(f"Подключился пользователь: {message.from_user.full_name}, id: {message.from_user.id}")
    await state.clear()

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await asyncio.sleep(1)

    if message.from_user.id in ADMIN_ID:
        keyboard = start_admin_reply_keyboard
        await state.set_state(AdminToolsModule.main_state_admin)
    else:
        keyboard = start_client_reply_keyboard
        await state.set_state(ClientToolsModule.main_state_client)

        now_date = datetime.datetime.now(pytz.utc).strftime(format="%d-%m-%Y %H:%M:%S")

        user_tg_id = message.from_user.id
        try:
            async with moto_db:
                user_db_id = await moto_db.test_user(user_tg_id=user_tg_id)
                if user_db_id:
                    if not await moto_db.change_user_visit_field(user_id=user_db_id, date_of_last_visit=now_date):
                        print(f"Не получилось внести сведения о посещении для пользователя {user_db_id} в БД")

                else:
                    await moto_db.save_new_user(created_at=now_date, user_tg_id=user_tg_id)

        except Exception as ex:
            print(f"Ошибка при занесении посещения в БД: {ex}")

    await message.answer(text="👋 Привет! Я — ваш виртуальный помощник по продаже мотоциклов, мопедов и запчастей. "
                              "Здесь вы сможете найти идеальный транспорт для себя, а также все необходимые компоненты "
                              "для его обслуживания.\n🚴‍♂️ Что я могу вам предложить?\n\n•	📦 Широкий выбор мотоциклов "
                              "и мопедов — новые и б/у модели от известных брендов.\n•	🔧 Запчасти и аксессуары — "
                              "все, что нужно для вашего двухколесного друга.\n•	💰 Специальные предложения и акции "
                              "— следите за нашими скидками и выгодными условиями.\n🌟 Начните прямо сейчас!\n\n"
                              "🚀 Давайте отправимся в ваше новое приключение на двух колесах!",
                         reply_markup=keyboard,
                         parse_mode=ParseMode.HTML)


@router.message(default_state)
async def default_empty_message(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.main_state_admin)
    if message.from_user.id in ADMIN_ID:
        keyboard = start_admin_reply_keyboard
    else:
        keyboard = start_client_reply_keyboard
    await message.answer(text="Неизвестная команда. Попробуйте сначала использовать команду /start.",
                         reply_markup=keyboard
                         )
