from aiogram.filters import CommandStart, Command
from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

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

    print("cancel button")
    current_state = await state.get_state()
    print(f"current state = {current_state}")

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

    await message.answer(text=text,
                         reply_markup=keyboard)


@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    print(f"Подключился пользователь: {message.from_user.full_name}, id: {message.from_user.id}")
    await state.clear()

    if message.from_user.id in ADMIN_ID:
        keyboard = start_admin_reply_keyboard
        await state.set_state(AdminToolsModule.main_state_admin)
        async with moto_db:
            await moto_db.make_db()
    else:
        keyboard = start_client_reply_keyboard
        await state.set_state(ClientToolsModule.main_state_client)
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
async def default_empty_message(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        keyboard = start_admin_reply_keyboard
    else:
        keyboard = start_client_reply_keyboard
    await message.answer(text="Неизвестная команда...",
                         reply_markup=keyboard
                         )
