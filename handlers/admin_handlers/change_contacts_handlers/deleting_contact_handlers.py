from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.reply_keyboard import get_keyboard
from config import moto_db
from utils.admin_change_callback import StorageForDeletingContacts

router = Router()


@router.callback_query(StorageForDeletingContacts.filter(F.reaction == "delete contact"))
async def deleting_photo_place_reaction(callback: CallbackQuery, callback_data: StorageForDeletingContacts):
    await callback.answer(text=f"Удаляем контакт.",
                          show_alert=False)
    await callback.message.edit_text(text="Контакт удален...", reply_markup=None)

    contact_id = callback_data.contact_id
    try:
        async with moto_db:
            await moto_db.delete_contact(contact_id=contact_id)
            text = "Контакт удален\nВыберите действие)👇:"
    except Exception as ex:
        print(f"Exception:\n{ex}")
        text = "Возникла ошибка при подключении к базе данных. Попробуйте позднее."

    keyboard = get_keyboard("Завершить",
                            placeholder="Выберите действие",
                            sizes=(1,))
    await callback.message.answer(text=text,
                                  reply_markup=keyboard)
