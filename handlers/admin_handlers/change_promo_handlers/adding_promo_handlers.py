from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from keyboards import build_choice_product_for_promo
from keyboards.reply_keyboard import get_keyboard, get_list_keyboard
from storage import AdminToolsModule

from config import moto_db
from user_filters import days_validate, date_validate, discount_validate

router = Router()


@router.message(AdminToolsModule.adding_promo, F.text)
async def adding_promo_title_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_promo_description)
    current_data = await state.get_data()
    current_promo_list = current_data["promo_list"]
    try:
        current_buttons_set = current_data["buttons_set"]
    except KeyError:
        current_buttons_set = []
    promo_title_index = 0
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo)
    await state.update_data(step=step)
    if message.text in current_buttons_set:
        for i in current_promo_list:
            if i[1] == message.text:
                promo_title_index = i[0]
        if promo_title_index != 0:
            await state.update_data(promo_title_name=message.text, promo_title_index=promo_title_index)
            text = f"Название акции: {markdown.hbold(message.text)} выбрано.\nВведите описание акции:"
            button_name = "Назад 🔙"
        else:
            text = f"Не удалось найти индекс акции: {message.text}"
            button_name = "Отмена 🔙"
    else:
        promo_title_name = message.text
        try:
            async with moto_db:
                saved_id = await moto_db.save_new_promo_title(promo_title_name)
                print(f"saved_id = {saved_id}")
                if saved_id:
                    await state.update_data(promo_title_name=promo_title_name, promo_title_index=saved_id[0])
                    text = f"Название акции: {markdown.hbold(message.text)} внесено в базу.\nВведите описание акции:"
                    button_name = "Назад 🔙"
                else:
                    text = "Не удалось записать название промо-акции в базу. Попробуйте позже."
                    button_name = "Отмена 🔙"
        except Exception as ex:
            print(f"Ошибка при записи названия промо-акции {ex}")
            text = "Не удалось записать название промо-акции в базу. Попробуйте позже."
            button_name = "Отмена 🔙"
    keyboard = get_keyboard(button_name)
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo)
async def wrong_adding_promo_title_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    try:
        current_buttons_set = current_data["buttons_set"]
    except KeyError:
        current_buttons_set = []
    current_buttons_set = list(current_buttons_set)
    current_buttons_set.append("Отмена 🔙")
    keyboard = get_list_keyboard(buttons=current_buttons_set, placeholder="Выберите название или введите вручную",
                                 sizes=(2,))
    await message.answer(text="Я Вас не понимаю. Выберите название акции или введите вручную.",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_description, F.text)
async def adding_promo_description_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_promo_discount)
    current_data = await state.get_data()
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo_description)
    await state.update_data(promo_description=message.text)
    text = f"Введено описание акции: {markdown.hbold(message.text)}.\nВведите скидку по акции (со знаком %):"
    button_name = "Назад 🔙"
    keyboard = get_keyboard(button_name, placeholder="Введите скидку (XX%)")
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_description)
async def wrong_adding_promo_description_handler(message: types.Message):
    keyboard = get_keyboard("Назад 🔙", placeholder="Введите описание промо-акции")
    await message.answer(text="Я Вас не понимаю. Введите описание акции.",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_discount, F.func(discount_validate).as_("discount"))
async def adding_promo_discount_handler(message: types.Message, state: FSMContext, discount: float):
    await state.set_state(AdminToolsModule.adding_promo_start_date)
    current_data = await state.get_data()
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo_discount)
    text = (f"Установлен размер скидки по акции: {markdown.hbold(discount) + '%'}.\nВведите дату начала акции "
            f"(если не устанавливать дату, то дата начала акции будет совпадать с датой активации):")
    keyboard = get_keyboard("Назад 🔙",
                            "Пропустить",
                            placeholder="Введите дату (dd.mm.yyyy)")
    await message.answer(text=text, reply_markup=keyboard)
    await state.update_data(promo_discount=discount)


@router.message(AdminToolsModule.adding_promo_discount)
async def wrong_adding_promo_discount_handler(message: types.Message):
    keyboard = get_keyboard("Назад 🔙", placeholder="Введите размер скидки (в процентах)")
    await message.answer(text="Я Вас не понимаю. Введите размер скидки (в процентах).",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_start_date, F.func(date_validate).as_("date_start"))
async def adding_promo_start_date_handler(message: types.Message, state: FSMContext, date_start: str):
    await state.set_state(AdminToolsModule.adding_promo_end_date)
    current_data = await state.get_data()
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo_start_date)
    text = f"Установлена дата начала акции: {markdown.hbold(date_start)}.\nВведите дату окончания акции:"
    button_name = "Назад 🔙"
    keyboard = get_keyboard(button_name, placeholder="Введите дату (dd.mm.yyyy)")
    await message.answer(text=text, reply_markup=keyboard)
    await state.update_data(promo_start_date=date_start)


@router.message(AdminToolsModule.adding_promo_start_date, F.text.casefold() == "пропустить")
async def adding_promo_skip_date_handler(message: types.Message, state: FSMContext):
    await state.set_state(AdminToolsModule.adding_promo_valid_length)
    current_data = await state.get_data()
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo_start_date)
    text = f"Дата начала акции: {markdown.hbold("не установлена")}.\nВведите количество дней действия акции:"
    button_name = "Назад 🔙"
    keyboard = get_keyboard(button_name, placeholder="Введите количество дней")
    await message.answer(text=text, reply_markup=keyboard)
    await state.update_data(promo_start_date="From activate")


@router.message(AdminToolsModule.adding_promo_start_date)
async def wrong_adding_promo_start_date_handler(message: types.Message):
    keyboard = get_keyboard("Назад 🔙", placeholder="Введите корректную дату (dd.mm.yyyy)")
    await message.answer(text="Я Вас не понимаю. Введите дату начала акции.",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_end_date, F.func(date_validate).as_("date_finish"))
async def adding_promo_end_date_handler(message: types.Message, state: FSMContext, date_finish: str):
    await state.set_state(AdminToolsModule.adding_promo_category)
    await state.update_data(promo_end_date=date_finish)
    current_data = await state.get_data()
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo_end_date)
    await state.update_data(promo_end_date=date_finish, category="category", valid_date_length=None)
    await __get_category_keyboard(state)
    current_data = await state.get_data()
    if current_data["buttons_category_names"]:
        button_name = current_data["buttons_category_names"]
        text = (f"Установлена дата окончания акции: {markdown.hbold(date_finish)}.\n"
                f"Выберите категорию товаров.")
        keyboard = get_list_keyboard(button_name, placeholder="Выберите категорию.")
    else:
        button_name = "Назад 🔙"
        text = (f"Установлена дата окончания акции: {markdown.hbold(date_finish)}.\n"
                f"Категории товаров для участия в промо-акции отсутствуют.")
        keyboard = get_keyboard(button_name, placeholder="Выберите действие.")
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_end_date)
async def wrong_adding_promo_end_date_handler(message: types.Message):
    keyboard = get_keyboard("Назад 🔙", placeholder="Введите дату (dd.mm.yyyy)")
    await message.answer(text="Я Вас не понимаю. Введите дату окончания акции.",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_valid_length, F.func(days_validate).as_("valid_days"))
async def valid_length_promo_handler(message: types.Message, state: FSMContext, valid_days: int):
    await state.set_state(AdminToolsModule.adding_promo_category)
    current_data = await state.get_data()
    step = current_data["step"]
    step.append(AdminToolsModule.adding_promo_valid_length)
    await state.update_data(promo_end_date=None, valid_date_length=valid_days, category="category")
    await __get_category_keyboard(state)
    current_data = await state.get_data()
    if current_data["buttons_category_names"]:
        button_name = set(current_data["buttons_category_names"].copy())
        text = (f"Установлена продолжительность промо-акции: {markdown.hbold(valid_days)} дней.\n"
                f"Выберите категорию товаров.")
        keyboard = get_list_keyboard(list(button_name), placeholder="Выберите действие.")
    else:
        button_name = "Назад 🔙"
        text = (f"Установлена продолжительность промо-акции: {markdown.hcode(valid_days)} дней.\n"
                f"Категории товаров для участия в промо-акции отсутствуют.")
        keyboard = get_keyboard(button_name, placeholder="Выберите действие.")
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_valid_length)
async def wrong_valid_length_promo_handler(message: types.Message):
    keyboard = get_keyboard("Назад 🔙", placeholder="Введите продолжительность промо-акции")
    await message.answer(text="Я Вас не понимаю.\nВведите продолжительность промо-акции.",
                         reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_category, F.text)
async def adding_promo_categories_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    button_name = current_data["buttons_category_names"]
    if message.text in button_name:
        await state.set_state(AdminToolsModule.adding_promo_sub_category)
        step = current_data["step"]
        step.append(AdminToolsModule.adding_promo_category)
        await state.update_data(category="sub_category")
        category_id = 0
        for i in current_data["buttons_category_list"]:
            print(f"i = {i}; i[1] = {i[1]}; text = {message.text}")
            if i[1].casefold() == message.text.casefold():
                category_id = i[0]
                break
            else:
                print(f"Can`t find category id!")
        await state.update_data(category_id=category_id)
        await __get_category_keyboard(state, category_id)
        current_data = await state.get_data()
        #  print(f"current data cat id: {current_data}")
        button_name = current_data["buttons_category_names"].copy()
        button_name.append("Отсутствует")
        button_name = set(button_name)
        if button_name:
            text = f"Вы выбрали категорию: {markdown.hbold(message.text)}.\nВыберите подкатегорию товара."
            keyboard = get_list_keyboard(list(button_name), placeholder="Выберите действие.")
        else:
            text = f"Вы выбрали категорию: {markdown.hbold(message.text)}.\nВыберите наименование товара."
            keyboard = get_list_keyboard(list(button_name), placeholder="Выберите действие.")
        await message.answer(text=text, reply_markup=keyboard)
    else:
        text = f"Указанной Вами категории нет в базе данных.\n Выберите категорию товаров."

        keyboard = get_list_keyboard(button_name.copy(), placeholder="Выберите категорию.")
        await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_category)
async def wrong_adding_promo_categories(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    button_name = set(current_data["buttons_category_names"].copy())
    if button_name:
        button_name = list(button_name)
        text = f"Я Вас не понимаю, выберите категорию товаров."
        keyboard = get_list_keyboard(button_name.copy(), placeholder="Выберите категорию.")
    else:
        button_name = "Назад 🔙"
        text = f"Отсутствуют категории товаров. Выберите действие."
        keyboard = get_keyboard(button_name, placeholder="Выберите категорию.")
    await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_sub_category, F.text)
async def adding_promo_subcategories_handler(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    button_name = current_data["buttons_category_names"]
    if message.text in button_name:
        await state.set_state(AdminToolsModule.adding_promo_product)
        step = current_data["step"]
        step.append(AdminToolsModule.adding_promo_sub_category)
        await state.update_data(category="products")
        sub_category_id = 0
        for i in current_data["buttons_category_list"]:
            print(f"i = {i}; i[1] = {i[1]}; text = {message.text}")
            if i[1].casefold() == message.text.casefold():
                sub_category_id = i[0]
                break
            else:
                print(f"Can`t find category id!")
        await state.update_data(sub_category_id=sub_category_id)
        await __get_category_keyboard(state,
                                      category_id=current_data["category_id"],
                                      sub_category_id=sub_category_id)

        current_data = await state.get_data()
        #  print(f"current data cat id: {current_data}")

        if current_data["buttons_category_list"]:
            text = "Выберите товары для добавления в промо-акцию ☝️."
            for i in current_data["buttons_category_list"]:
                product = i[1]
                keyboard = build_choice_product_for_promo(product_id=i[0], reaction="adding promo")
                await message.answer(text=product, reply_markup=keyboard)
            keyboard = get_keyboard("Завершить",
                                    placeholder="Выберите действие")
        else:
            text = "Не удается загрузить список товаров из базы. Попробуйте позже."

            keyboard = get_keyboard("Назад 🔙",
                                    placeholder="Выберите действие")
        await message.answer(text=text, reply_markup=keyboard)


@router.message(AdminToolsModule.adding_promo_sub_category)
async def wrong_adding_promo_subcategories(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    button_name = set(current_data["buttons_category_names"].copy())
    if button_name:
        button_name = list(button_name)
        text = f"Я Вас не понимаю, выберите подкатегорию товаров."
        keyboard = get_list_keyboard(button_name.copy(), placeholder="Выберите подкатегорию.")
    else:
        button_name = "Назад 🔙"
        text = f"Отсутствуют подкатегории товаров. Выберите действие."
        keyboard = get_keyboard(button_name, placeholder="Выберите категорию.")
    await message.answer(text=text, reply_markup=keyboard)


#  -----------Function for get category of products for buttons-----------
async def __get_category_keyboard(state: FSMContext, category_id: int = 0, sub_category_id: int = 0) -> None:
    current_data = await state.get_data()
    #  pprint(f"curr data in get category = {current_data}")
    if current_data["category"] == "category":
        try:
            async with moto_db:
                buttons_list = await moto_db.get_categories()
                #  print(f"Buttons_list_category = {buttons_list}")
        except Exception as ex:
            print(f"Error list_category: {ex}")
    elif current_data["category"] == "sub_category":
        try:
            async with moto_db:
                buttons_list = await moto_db.get_sub_categories(category_id=category_id)
                #  print(f"Buttons_list_subcat = {buttons_list}")
        except Exception as ex:
            print(f"Error list_sub_category: {ex}")
    elif current_data["category"] == "products":
        try:
            async with moto_db:
                buttons_list = await moto_db.get_products_for_promo(category_id=category_id,
                                                                    sub_category_id=sub_category_id)
                print(f"button_list in products after db request = {buttons_list}")
                if buttons_list is None:
                    buttons_list = []
                    print(f"Anything wrong: Buttons_list_product = {buttons_list}")
        except Exception as ex:
            print(f"Error list_products buttons: {ex}")

    buttons_text = [x[1] for x in buttons_list]
    await state.update_data(buttons_category_list=buttons_list.copy(), buttons_category_names=buttons_text.copy())


# ---------------FINISH BLOCK--------------------
'''
    text = f"Вы внесли следующие данные:\n\n"
    text += f"{markdown.hbold(current_data['promo_title_name'])}\n\n"
    text += f"{current_data['promo_description']}\n\n"
    text += f"Размер скидки: {current_data['promo_discount']}\n"
    if current_data["promo_start_date"] == "From activate":
        text += (f"промо-акция начнет действовать с момента активации и продлится:"
                 f" {markdown.hcode(current_data['promo_valid_length'])}\n")
    else:
        text += f"Дата начала акции: {current_data['promo_start_date']}\n"
        text += f"Дата окончания акции: {current_data['promo_end_date']}\n"

    keyboard = get_keyboard("Назад 🔙",
                            "Записать в базу 💽",
                            placeholder="Выберите действие")
    await message.answer(text=text, reply_markup=keyboard)
'''
