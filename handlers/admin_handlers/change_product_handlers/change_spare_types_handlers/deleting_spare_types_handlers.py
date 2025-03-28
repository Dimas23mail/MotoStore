from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_reply_keyboards import admin_finish_action
from storage import AdminToolsModule

from config import moto_db
from utils import StorageForDeletingCategory

router = Router()


@router.callback_query(StorageForDeletingCategory.filter(F.reaction == "delete spare_types"))
async def deleting_product_spare_types_reaction(callback: CallbackQuery, callback_data: StorageForDeletingCategory,
                                                state: FSMContext):
    await callback.answer(text=f"Удаляем вид з/ч",
                          show_alert=False)
    await callback.message.edit_text(text="Вид удален...", reply_markup=None)
    print(f"Перехватили удаление вида з/ч...")
    category_id = callback_data.category_id

    try:
        async with moto_db:
            await moto_db.deleting_spare_types(category_id)
            text = "Вид запасных частей удален\nВыберите действие)👇:"
    except Exception as ex:
        print(f"Exception:\n{ex}")
        text = "Возникла ошибка при подключении к базе данных. Попробуйте позднее."

    keyboard = admin_finish_action
    await callback.message.answer(text=text,
                                  reply_markup=keyboard)

    await state.set_state(AdminToolsModule.deleting_spare_types)
