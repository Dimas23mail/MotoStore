from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import admin_change_contact, admin_finish_action
from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule
from user_filters import telephone_validate
from config import moto_db
from utils import make_string_for_output, StorageForAddingPromoProducts

router = Router()


@router.callback_query(StorageForAddingPromoProducts.filter(F.reaction == "adding promo"))
async def adding_promo_reaction(callback: CallbackQuery, callback_data: StorageForAddingPromoProducts,
                                state: FSMContext) -> None:
    await callback.answer(text=f"Добавляем промо товару.",
                          show_alert=False)
    #  await callback.message.edit_text(text="Контакт в статусе изменения...", reply_markup=None)

    product_id = callback_data.product_id
    await state.update_data(product_id=product_id)

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
