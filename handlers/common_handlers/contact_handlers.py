from aiogram import F, types, Router

from aiogram.fsm.context import FSMContext

from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule, ClientToolsModule
from config import moto_db
from utils import make_string_for_output

router = Router()


@router.message(AdminToolsModule.main_state_admin, F.text.casefold() == "контакты ☎️ 📱")
@router.message(ClientToolsModule.main_state_client, F.text.casefold() == "контакты ☎️ 📱")
async def check_client_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is AdminToolsModule.main_state_admin:
        await state.set_state(AdminToolsModule.contact_info)
    elif current_state is ClientToolsModule.main_state_client:
        await state.set_state(ClientToolsModule.contact_info)
    keyboard = get_keyboard("Завершить",
                            placeholder="Выберите действие",
                            sizes=(1,))
    text = "Контактная информация для связи с нами:"
    await message.answer(text=text, reply_markup=keyboard)

    try:
        async with moto_db:
            contacts_list = await moto_db.get_all_contacts()
            if contacts_list:
                for element in contacts_list:
                    text = make_string_for_output(source=element[1:])

                    await message.answer(text=text)

            else:
                text = "В базе данных отсутствуют контакты."
    except Exception as ex:
        print(f"Exception in change contacts: {ex}")
