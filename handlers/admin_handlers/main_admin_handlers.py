from aiogram import F, types, Router

from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from keyboards.admin_reply_keyboards import admin_change_contact_menu
from storage import AdminToolsModule
from keyboards import admin_main_menu, admin_change_products_menu, admin_change_promo_menu, \
    admin_change_category_products

router = Router()


@router.message(AdminToolsModule.main_state_admin, F.text.casefold() == "админ-панель 🛠")
async def check_admin_command(message: types.Message, state: FSMContext) -> None:
    keyboard = admin_main_menu
    await state.set_state(AdminToolsModule.main_menu_admin)
    await message.answer(
        text="Вы находитесь в панели администратора,\nвыберите действие 👇:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.main_menu_admin, F.text.casefold() == "изменить наши товары 🏍 🛵 🔧",
                F.from_user.id.in_(ADMIN_ID))
async def change_our_products_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_products_menu)
    keyboard = admin_change_products_menu
    await message.answer(
        text="Вы перешли в меню изменения информации о наших товарах. Выберите действие 👇:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.main_menu_admin, F.text.casefold() == "изменить промо-акции 🎁",
                F.from_user.id.in_(ADMIN_ID))
async def change_our_promo_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_promo_menu)
    keyboard = admin_change_promo_menu
    await message.answer(
        text="Вы перешли в меню изменения информации о площадках. Выберите действие 👇:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.main_menu_admin, F.text.casefold() == "изменить контакты ☎️ 📱",
                F.from_user.id.in_(ADMIN_ID))
async def change_contacts_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_contact_menu)
    keyboard = admin_change_contact_menu
    await message.answer(
        text="Вы перешли в меню изменения контактной информации. Выберите действие 👇:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.main_menu_admin, F.text.casefold() == "изменить категории товаров",
                F.from_user.id.in_(ADMIN_ID))
async def change_contacts_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AdminToolsModule.change_category_menu)
    keyboard = admin_change_category_products
    await message.answer(
        text="Вы перешли в меню изменения категорий товаров. Выберите действие 👇:",
        reply_markup=keyboard
    )


@router.message(AdminToolsModule.main_menu_admin)
async def wrong_change_menu(message: types.Message) -> None:
    keyboard = admin_main_menu
    await message.answer(
        text="Я Вас не понимаю. Выберите действие 👇:",
        reply_markup=keyboard
    )
