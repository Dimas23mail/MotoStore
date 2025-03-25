from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import moto_db
from keyboards import admin_change_place_info
from keyboards.reply_keyboard import get_keyboard
from storage import AdminToolsModule
from utils import StorageForChangePlaceData, StorageForChangeImageData, deleting_photo_from_list

router = Router()


@router.message(Command("back"))
@router.message(F.text.casefold() == "назад")
@router.message(F.text.casefold() == "назад 🔙")
@router.message(F.text.casefold() == "back")
async def back_adding_place_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    current_step_list = current_data["step"]
    caption = ""
    text = "не попал в state"
    button_name = "Отмена 🔙"
    current_step = current_step_list.pop()
    if current_step in (AdminToolsModule.input_place_name,):
        caption = "Введите название площадки:"
        text = "Вы отменили ввод. Введите название площадки:"
    elif current_step in (AdminToolsModule.input_place_description,):
        caption = "Введите краткое описание площадки:"
        text = "Вы отменили ввод. Введите краткое описание площадки:"
        button_name = "Назад 🔙"
    elif current_step in (AdminToolsModule.input_place_city,):
        caption = "Введите название города:"
        text = "Вы отменили ввод. Введите название города:"
        button_name = "Назад 🔙"
    elif current_step in (AdminToolsModule.input_place_address,):
        caption = "Введите адрес:"
        text = "Вы отменили ввод. Введите адрес:"
        button_name = "Назад 🔙"
    elif current_step in (AdminToolsModule.input_place_telephone,):
        caption = "Введите телефон:"
        text = "Вы отменили ввод. Введите телефон:"
        button_name = "Назад 🔙"

    await state.set_state(current_step)
    keyboard = get_keyboard(button_name,
                            placeholder=caption,
                            sizes=(1,))
    await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(StorageForChangePlaceData.filter(F.reaction == "change place"))
async def change_place_button_reaction(callback: CallbackQuery, callback_data: StorageForChangePlaceData,
                                       state: FSMContext):
    await callback.answer(text=f"Вносим изменение в информацию о площадке.",
                          show_alert=False)
    current_data = await state.get_data()
    if current_data["has_photo"]:
        await callback.message.edit_caption(caption="Вносятся изменения в информацию о площадке...", reply_markup=None)

    keyboard = admin_change_place_info
    await callback.message.answer(text="Какую информацию Вы хотите изменить\n(выберите пункт меню)👇:",
                                  reply_markup=keyboard)
    await state.update_data(place_id=callback_data.place_id)
    await state.set_state(AdminToolsModule.start_change_place)


@router.callback_query(StorageForChangeImageData.filter(F.reaction == "delete photo"))
async def deleting_photo_place_reaction(callback: CallbackQuery, callback_data: StorageForChangeImageData,
                                        state: FSMContext):
    await callback.answer(text=f"Вносим изменение в фотографии.",
                          show_alert=False)
    await callback.message.edit_caption(caption="Фотография удалена...", reply_markup=None)
    #  print(f"Перехватили удаление...")
    place_id = callback_data.place_id
    element_id = callback_data.photo_id
    current_data = await state.get_data()
    photo_list = current_data["list_photos"]
    photo_string = deleting_photo_from_list(photo_list=photo_list, photo_id=element_id)
    try:
        async with moto_db:
            await moto_db.change_place_photos(photo_string, place_id)
            text = "Фотография удалена\nВыберите действие)👇:"
    except Exception as ex:
        print(f"Exception:\n{ex}")
        text = "Возникла ошибка при подключении к базе данных. Попробуйте позднее."

    keyboard = get_keyboard("Закончить",
                            placeholder="Выберите действие",
                            sizes=(1,))
    await callback.message.answer(text=text,
                                  reply_markup=keyboard)
    #  Установить нужный state
    await state.set_state(AdminToolsModule.change_place_photo)


@router.callback_query(StorageForChangeImageData.filter(F.reaction == "delete place"))
async def deleting_place_reaction(callback: CallbackQuery, callback_data: StorageForChangeImageData, state: FSMContext):
    await callback.answer(text=f"Удаляем площадку",
                          show_alert=False)
    await callback.message.edit_caption(caption="Площадка удалена...", reply_markup=None)
    print(f"Перехватили удаление place...")
    place_id = callback_data.place_id

    try:
        async with moto_db:
            await moto_db.deleting_place(place_id)
            text = "Площадка удалена\nВыберите действие)👇:"
    except Exception as ex:
        print(f"Exception:\n{ex}")
        text = "Возникла ошибка при подключении к базе данных. Попробуйте позднее."

    keyboard = get_keyboard("Завершить",
                            placeholder="Выберите действие",
                            sizes=(1,))
    await callback.message.answer(text=text,
                                  reply_markup=keyboard)
    #  Установить нужный state
    await state.set_state(AdminToolsModule.deleting_place)
