from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from keyboards import cancel_keyboard, admin_change_spare_parts_products
from storage import AdminToolsModule

from config import moto_db


router = Router()


@router.message(AdminToolsModule.adding_spare_types, F.text)
async def adding_product_spare_types_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.change_spare_types_menu)
    try:
        async with moto_db:
            if await moto_db.save_category(category=message.text):
                text = f"Наименование вида: {message.text}, внесено в базу данных."
            else:
                text = "Возникла ошибка при передаче данных в базу. Попробуйте позднее."
        keyboard = admin_change_spare_parts_products
    except Exception as ex:
        print(f"Exception in adding_category module: {ex}")
        text = "Возникла ошибка при обращении к базе данных. Попробуйте позднее."
        keyboard = admin_change_spare_parts_products
    await message.answer(text=text,
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_spare_types)
async def wrong_adding_product_spare_types_handler(message: types.Message):
    keyboard = cancel_keyboard
    await message.answer(text="Я Вас не понимаю, введите текстовое название категории товаров:",
                         reply_markup=keyboard)
