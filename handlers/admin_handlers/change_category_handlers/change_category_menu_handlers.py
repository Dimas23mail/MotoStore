from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from keyboards import cancel_keyboard, delete_record_ikb
from keyboards.admin_reply_keyboards import admin_finish_action, admin_change_category_products

from storage import AdminToolsModule
from config import moto_db

router = Router()


@router.message(AdminToolsModule.change_category_menu, F.text.casefold() == "добавить категорию ➕")
async def adding_product_category_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_category)
    keyboard = cancel_keyboard
    await message.answer(text="Введите название категории:",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.change_category_menu, F.text.casefold() == "удалить категорию ❌")
async def deleting_product_category_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.deleting_category)
    try:
        async with moto_db:
            categories = await moto_db.get_categories()
        for element in categories:
            keyboard = delete_record_ikb(record_id=element[0], reaction="delete category")
            await message.answer(text=element[-1], reply_markup=keyboard)
        text = "Выберите категорию товаров для удаления ☝️:"
        keyboard = admin_finish_action
    except Exception as ex:
        print(f"Exception in adding_category module: {ex}")
        text = "Возникла ошибка при обращении к базе данных. Попробуйте позднее."
        keyboard = admin_change_category_products
    await message.answer(text=text,
                         reply_markup=keyboard)


@router.message(AdminToolsModule.change_category_menu)
async def wrong_change_product_category_menu_handler(message: types.Message, state: FSMContext):
    await message.answer(text="Error! Category product menu handler!")
