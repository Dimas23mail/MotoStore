from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from keyboards import cancel_keyboard, admin_change_category_products
from storage import AdminToolsModule

from config import moto_db


router = Router()


@router.message(AdminToolsModule.change_contact_menu, F.text.casefold() == "изменить контактные данные 📄")
async def adding_contact_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.change_contact_main)
    await message.answer(text="Вы перешли в меню изменения контактных данных.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.change_contact_menu, F.text.casefold() == "добавить данные ➕")
async def adding_contact_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_contact_title)
    await state.update_data(step=[AdminToolsModule.change_contact_menu,])
    await message.answer(text="Вы перешли в меню добавления контактных данных.\nВведите название магазина.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.change_contact_menu, F.text.casefold() == "удалить данные ❌")
async def adding_contact_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.delete_contact_main)
    await message.answer(text="Вы перешли в меню удаления контактных данных.",
                         reply_markup=cancel_keyboard)


@router.message(AdminToolsModule.change_contact_menu)
async def wrong_adding_contact_menu_handler(message: types.Message):
    await message.answer(text="Я Вас не понимаю.\nВведите название магазина.",
                         reply_markup=cancel_keyboard)
