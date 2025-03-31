import datetime

import pytz
from aiogram import F, types, Router

from aiogram.fsm.context import FSMContext

from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule, ClientToolsModule
from config import moto_db
from utils import make_promo_string

router = Router()


@router.message(AdminToolsModule.main_state_admin, F.text.casefold() == "акции и скидки 💰")
@router.message(ClientToolsModule.main_state_client, F.text.casefold() == "акции и скидки 💰")
async def check_client_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is AdminToolsModule.main_state_admin:
        await state.set_state(AdminToolsModule.promo_info)
    elif current_state is ClientToolsModule.main_state_client:
        await state.set_state(ClientToolsModule.promo_info)
    text = "В настоящее время мы проводим следующие промо-акции:"
    await message.answer(text=text)
    now_date = datetime.datetime.now(pytz.utc).strftime(format="%d-%m-%Y %H:%M:%S")

    try:
        async with moto_db:
            promo_list = await moto_db.get_all_promo_by_date(now_date=now_date)
            if promo_list:
                for element in promo_list:
                    text = make_promo_string(source=element)
                    await message.answer(text=text)
                text = "Выберите промо-акцию."
            else:
                text = "В настоящее время промо-акции отсутствуют."
    except Exception as ex:
        print(f"Exception in change contacts: {ex}")
        text = "Возникли проблемы при подключении к базе промо-акций. Попробуйте позднее."
    keyboard = get_keyboard("Завершить",
                            placeholder="Выберите действие",
                            sizes=(1,))
    await message.answer(text=text, reply_markup=keyboard)
