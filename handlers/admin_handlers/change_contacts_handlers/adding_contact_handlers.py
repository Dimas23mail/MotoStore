from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from keyboards import cancel_keyboard
from keyboards.admin_reply_keyboards import admin_change_contact_menu
from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule
from user_filters import telephone_validate
from config import moto_db
from utils import make_string_for_output

router = Router()


@router.message(AdminToolsModule.adding_contact_title, F.text)
async def adding_contact_title_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    current_step = current_data["step"]
    current_step.append(AdminToolsModule.adding_contact_title)
    await state.update_data(contact_title=message.text, step=current_step)
    keyboard = get_keyboard("Назад 🔙",
                            placeholder="Введите город",
                            sizes=(1,))
    await state.set_state(AdminToolsModule.adding_contact_city)
    await message.answer(
        text="Название нового магазина добавлено.\nВведите город магазина:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.adding_contact_title)
async def wrong_adding_contact_title_handler(message: types.Message):
    await message.answer(text="Я Вас не понимаю.\nВведите название магазина.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.adding_contact_city, F.text)
async def adding_contact_city_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    current_step = current_data["step"]
    current_step.append(AdminToolsModule.adding_contact_city)
    await state.update_data(contact_city=message.text, step=current_step)
    keyboard = get_keyboard("Назад 🔙",
                            placeholder="Введите адрес",
                            sizes=(1,))
    await state.set_state(AdminToolsModule.adding_contact_address)
    await message.answer(
        text="Город нового магазина добавлен.\nВведите адрес магазина:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.adding_contact_city)
async def wrong_adding_contact_city_handler(message: types.Message):
    await message.answer(text="Я Вас не понимаю.\nВведите город магазина.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.adding_contact_address, F.text)
async def adding_contact_city_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    current_step = current_data["step"]
    current_step.append(AdminToolsModule.adding_contact_address)
    await state.update_data(contact_address=message.text, step=current_step)
    keyboard = get_keyboard("Назад 🔙",
                            placeholder="+7(999)999-99-99",
                            sizes=(1,))
    await state.set_state(AdminToolsModule.adding_contact_phone)
    await message.answer(
        text="Адрес нового магазина добавлен.\nВведите телефон магазина:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.adding_contact_address)
async def wrong_adding_contact_city_handler(message: types.Message):
    await message.answer(text="Я Вас не понимаю.\nВведите адрес магазина.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.adding_contact_phone, F.func(telephone_validate).as_("phone"))
async def adding_contact_phone_handler(message: types.Message, state: FSMContext, phone: str = ""):
    await state.update_data(contact_phone=phone, step=[AdminToolsModule.change_contact_menu,])
    current_data = await state.get_data()
    text_tuple = (current_data["contact_title"], current_data["contact_city"], current_data["contact_address"],
                  current_data["contact_phone"])
    await state.set_state(AdminToolsModule.change_contact_menu)
    keyboard = admin_change_contact_menu
    try:
        async with moto_db:
            if await moto_db.save_contacts(source_tuple=text_tuple):
                text = (f"Контактные данные:\n{make_string_for_output(source=text_tuple)}\n\nдобавлены в базу.\n"
                        f"Выберите действие 👇:")
            else:
                text = "Возникла ошибка при обращении к БД. Попробуйте позже."
    except Exception as ex:
        print(f"Exception: {ex}")
        text = "Возникла ошибка при записи контактных данных в базу данных. Попробуйте позже."
    await message.answer(
        text=text,
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.adding_contact_phone)
async def wrong_adding_contact_phone_handler(message: types.Message):
    await message.answer(text="Я Вас не понимаю.\nВведите телефон магазина.",
                         reply_markup=cancel_keyboard)
