from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from keyboards import cancel_keyboard, action_with_record_ikb, admin_change_spare_parts_products
from keyboards.admin_reply_keyboards import admin_finish_action, admin_change_category_products

from storage import AdminToolsModule
from config import moto_db

router = Router()


@router.message(AdminToolsModule.change_spare_types_menu, F.text.casefold() == "добавить вид 🔧 ➕")
async def adding_product_spare_types_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_spare_types)
    keyboard = cancel_keyboard
    await message.answer(text="Введите название вида запасных частей:",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.change_spare_types_menu, F.text.casefold() == "удалить вид 🔧 ❌")
async def deleting_product_spare_types_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.deleting_spare_types)
    try:
        async with moto_db:
            spare_types = await moto_db.get_spare_types()
        for element in spare_types:
            keyboard = action_with_record_ikb(record_id=element[0], reaction="delete spare_types")
            await message.answer(text=element[-1], reply_markup=keyboard)
        text = "Выберите вид запасных частей для удаления ☝️:"
        keyboard = admin_finish_action
    except Exception as ex:
        print(f"Exception in adding_category module: {ex}")
        text = "Возникла ошибка при обращении к базе данных. Попробуйте позднее."
        keyboard = admin_change_category_products
    await message.answer(text=text,
                         reply_markup=keyboard)


@router.message(AdminToolsModule.change_spare_types_menu)
async def wrong_change_product_spare_types_menu_handler(message: types.Message):
    keyboard = admin_change_spare_parts_products
    await message.answer(text="Я Вас не понимаю.\nВыберите пункт меню 👇:", reply_markup=keyboard)
