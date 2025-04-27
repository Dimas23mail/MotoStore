import asyncio
import os
import datetime
from dataclasses import astuple

from aiogram import types

from .files_worker import make_tuples_from_xml
from .xml_parse import parse_xml
from .dict_parse import (product_group_dict_parse, products_dict_parse, storages_parse, products_in_storages_parse)
from .compare_utils import compare_tuple_lists
from config import moto_db, bot, PRIVATE_CHAT_ID
from storage import ValidateFieldsForDb, StoragesFields, ProductsForStoragesDB, ProductsForStoragesCompare


async def updating_db_from_xml() -> str | None:
    #  Get two tuples of files: (image_files, xml_files)
    tuples_of_new_files = make_tuples_from_xml()
    text = ""
    if tuples_of_new_files:
        print(f"tuples_of_xml:\n{tuples_of_new_files[1]}")
        for i in tuples_of_new_files[1]:
            #  Get parse xml_data from files
            result_dict = parse_xml(str(os.getcwd()) + "/xml_base/" + i)
            #  print(f"result dict in appending:\n{result_dict}")
            print("*" * 100)
            #  Testing xml_files (to be or not two beer)
            if ("КоммерческаяИнформация" in result_dict.keys() and "Классификатор" in
                    result_dict["КоммерческаяИнформация"].keys()):
                #  Find products xml_file (if true) and storage (if else)
                if "Группы" in result_dict["КоммерческаяИнформация"]["Классификатор"].keys():
                    print("Groups")
                    # Get list of category of products
                    result_list_category = product_group_dict_parse(source=result_dict)
                    # Get list of products
                    result_list_products = products_dict_parse(source=result_dict)

                    #  Updating categories in DB
                    if await updating_categories_db(source_category=result_list_category.copy()):
                        text = "Загрузка данных в подкатегории прошла успешно."
                        print(text)
                    print("*" * 100)
                    #  Updating products in DB (Insert, Append, Update)
                    products_list = await updating_products_db(source_products=result_list_products.copy(),
                                                               list_of_photo=tuples_of_new_files[0].copy())
                    #  print(f"product_list = {products_list}")
                    if products_list:
                        text = "Загрузка данных в товары прошла успешно."
                        print(text)
                        print("*" * 100)

                elif "ПакетПредложений" in result_dict["КоммерческаяИнформация"].keys():

                    result_products_in_storages = products_in_storages_parse(result_dict)
                    #  print(f"result product in storages: {result_products_in_storages}")
                    need_for_changing = await updating_products_in_storage_db(source_list=result_products_in_storages)
                    if need_for_changing[0]:
                        text = "Загрузка информации о количестве товаров складах"
                        print(f"{text}, result: {need_for_changing}")
                        print("*" * 100)
                    if need_for_changing[1]:
                        text = "Обновление информации о количестве товаров складах"
                        print(f"{text}, result: {need_for_changing}")
                        print("*" * 100)

                    result_storage_list = storages_parse(result_dict)
                    need_for_changing = await updating_storage_db(source_list=result_storage_list)
                    if result_storage_list:
                        text = "Загрузка информации о складах"
                        print(f"{text}, result: {need_for_changing}")
                        print("*" * 100)

                else:
                    text = f"Проблемы с расшифровкой xml-файла: {i}"
                    return text
            else:
                return "Формат xml файлов не соответствует образцу!"
    else:
        return text if text else None  # "Новые файлы отсутствуют."


def validate_data_from_storage(source: list) -> list[StoragesFields]:
    data_storage_list = []
    for i in source:
        storage = StoragesFields()
        storage.id_1c = i[0]
        storage.title = i[1]
        storage.address = i[2]
        data_storage_list.append(storage)
    return data_storage_list


def validate_products_for_storages(source: list) -> list[ProductsForStoragesDB]:
    data_products_for_storages = []
    for i in source:
        storage = ProductsForStoragesDB()
        storage.id_products = i[0]
        storage.storage_id = i[1]
        storage.counts = i[2]
        storage.costs_for_pce = i[3]
        storage.date_of_change = i[4]
        data_products_for_storages.append(storage)
    return data_products_for_storages


def validate_products_for_compare(source: list) -> list[ProductsForStoragesCompare]:
    data_products_for_storages = []
    for i in source:
        storage = ProductsForStoragesCompare()
        storage.counts = i[0]
        storage.costs_for_pce = i[1]
        storage.date_of_change = i[2]
        storage.key = i[3]
        data_products_for_storages.append(storage)
    return data_products_for_storages


async def updating_products_in_storage_db(source_list: list) -> tuple:
    #  print(f"source:\n{source_list}")
    #  storages_list = [("id_product_1c",                       "id_storage_1c", "quantity", "price_for_pce"), ]
    #                    '8eb6bb44-b57e-11e3-8adc-00252231065e', None,            None,       '0'
    # DB: products_in_storages_db = (id, id_products, storage_id, counts, costs_for_pce, date_of_change)
    # Запрашиваем из БД product_id и id_1c (для их сопоставления)
    async with moto_db:
        product_id_from_db = await moto_db.get_products_id()

    product_id_from_db = {i[0]: i[1] for i in product_id_from_db}
    #  print(f"product_id_from_db:\n{product_id_from_db}")

    # Запрашиваем из БД storages_id и id_1c (для их сопоставления)
    async with moto_db:
        storages_id_from_db = await moto_db.get_storages_id()
    storages_id_from_db = {i[0]: i[1] for i in storages_id_from_db}

    #  Готовим данные (преобразовываем типы) из xml для модуля сравнения -> список с полями как в БД
    products_in_storage = []
    actual_date = datetime.datetime.now().strftime("%x %X")
    for i in source_list:
        products_id = str(product_id_from_db[i[0]])
        id_storage = str(storages_id_from_db[i[1]]) if isinstance(i[1], str) else "1"
        try:
            if not (i[2] is None):
                counts = int(i[2])
            else:
                counts = 0
        except ValueError:
            counts = 0
        try:
            if not (i[3] is None):
                costs_for_pce = float(i[3])
            else:
                costs_for_pce = 0.0
        except ValueError:
            costs_for_pce = 0.0
        date_of_change = actual_date
        line = (counts, costs_for_pce, date_of_change, products_id + " " + id_storage)
        #  print(f"line = {line}")
        products_in_storage.append(line)
    #  print(f"products_in_storage:\n{products_in_storage}")

    #  Валидируем эти данные по dataclass для сравнения
    valid_list_products_in_storage = validate_products_for_compare(products_in_storage.copy())
    #  print(f"valid list product:\n{valid_list_products_in_storage}")

    #  Загружаем из БД данные о товарах на хранении
    async with moto_db:
        products_from_storage_db = await moto_db.get_all_products_from_storage()

    #  Готовим поля к валидации для сравнения
    for_validate_list_db = []
    for i in products_from_storage_db:
        key = str(i[0]) + " " + str(i[1])
        for_validate_list_db.append((int(i[2]), float(i[3]), i[4], key))

    #  Валидируем поля для сравнения
    validate_list_from_db = validate_products_for_compare(for_validate_list_db)
    #  print(f"validate_list_from_db:\n{validate_list_from_db}")

    #  Сравниваем список товаров из БД и из xml в результате ->
    #  -> compared_tuple: ([list data to inserting], [list data fo updating])
    compared_tuple = compare_tuple_lists(db_list=validate_list_from_db.copy(),
                                         maked_list=valid_list_products_in_storage.copy(),
                                         field_key='key',
                                         field_skip=['date_of_change',])
    print(f"compared lists:\n{compared_tuple}")
    # -----------------------------------------
    print(f"Lists - compared!")
    print("-" * 100)

    if compared_tuple[0]:
        list_to_inserting = []
        for i in compared_tuple[0]:
            #  print(f"i = {i}")
            #  print(f"i.counts = {i.counts}, type = {type(i.counts)}")
            line = (int(i.key.split()[0]), int(i.key.split()[1]), i.counts, i.costs_for_pce, i.date_of_change)
            list_to_inserting.append(line)
    else:
        list_to_inserting = None
    #  print(f"list_to_inserting:\n{list_to_inserting}")

    if compared_tuple[1]:
        list_to_updating = []
        for i in compared_tuple[1]:
            line = (i.counts, i.costs_for_pce, i.date_of_change, int(i.key.split()[0]), int(i.key.split()[1]))
            list_to_updating.append(line)
    else:
        list_to_updating = None
    #  print(f"list_to_updating before converting:\n{list_to_updating}")
    result_insert, result_update = None, None
    if list_to_inserting:
        async with moto_db:
            result_insert = await moto_db.appending_products_in_storage(source_list=list_to_inserting.copy())

    if list_to_updating:
        async with moto_db:
            result_update = await moto_db.appending_products_in_storage(source_list=list_to_updating.copy())
    #  print(f"list_to_inserting:\n{list_to_inserting}\n\nlist_to_updating:\n{list_to_updating}")
    return result_insert, result_update


async def updating_storage_db(source_list: list) -> bool:
    result = False
    source_storage = validate_data_from_storage(source=source_list[1:])

    async with moto_db:
        storage_from_db = await moto_db.get_all_storages()

    if len(storage_from_db) > 0:
        storage_from_db = validate_data_from_storage(source=storage_from_db)
    result_compare = compare_tuple_lists(db_list=storage_from_db, maked_list=source_storage, field_key="id_1c")

    if result_compare[0]:
        # appending data function
        storages_list = []
        for i in result_compare[0]:
            storages_list.append(astuple(i))
        try:
            async with moto_db:
                result = await moto_db.appending_storages(storages_list=storages_list)
        except Exception as ex:
            print(f"Exception adding storages in DB: {ex}")

    elif result_compare[1]:
        # updating data function
        storages_list = []
        for i in result_compare[0]:
            storages_list.append(i.convert_class_to_tuple_for_update())
        try:
            async with moto_db:
                result = await moto_db.updating_storages(storages_list=storages_list)
        except Exception as ex:
            print(f"Exception updating storages in DB: {ex}")
    else:
        print(f"result: Null")
    return result


async def updating_products_db(source_products: list[tuple], list_of_photo: list) -> bool:
    print("in updating prod db")
    async with moto_db:
        products_from_db = await moto_db.get_all_products_wo_id()
        sub_category = await moto_db.get_all_sub_categories()
    list_in_db = prepare_products_list(source_products=source_products.copy(), list_of_photo=list_of_photo.copy(),
                                       sub_category=sub_category.copy())
    print(f"list is ok")
    #  print(products_from_db)
    validate_product_from_db = validate_data_from_db(source_list=products_from_db.copy())
    print("validate is ok")
    compared_tuple = compare_tuple_lists(db_list=validate_product_from_db.copy(), maked_list=list_in_db.copy(),
                                         field_key="id_1c", field_skip=["created_at", "image_url"])

    response = False
    if len(compared_tuple[0]) > 0:
        print(f"Adding new products!")
        save_list = [astuple(x) for x in compared_tuple[0]]
        async with moto_db:
            response = await moto_db.insert_products_from_xml(products_list=save_list.copy())
        print(f"Writing products in DB!")

    if len(compared_tuple[1]) > 0:
        print(f"Change fields of products!")
        save_list = [x.convert_class_to_tuple_for_update() for x in compared_tuple[1]]
        print(f"save_list = {save_list[:2]}")
        async with moto_db:
            response = await moto_db.update_products_from_xml(products_list=save_list.copy())
        print(f"Compared list not null! Writing missing data list!")

    if len(compared_tuple[0]) == 0 and len(compared_tuple[1]) == 0:
        print(f"Missing new data in xml")

    #  i = await send_photo_into_channel(list_of_photo=list_of_photo)
    #  не забыть: фотки бывают по несколько штук на один товар, нужно писать списком

    # не забыть: пропустить поля с фотками, если в photo_url есть ТГ id

    return response


def validate_data_from_db(source_list: list[tuple]) -> list:
    result_list = []
    for element in source_list:
        fields_for_db = ValidateFieldsForDb()
        fields_for_db.category_id = element[0]
        fields_for_db.sub_category_id = element[1]
        fields_for_db.title = element[2]
        fields_for_db.brand = element[3]
        fields_for_db.description = element[4]
        fields_for_db.image_url = element[5]
        fields_for_db.created_at = element[6]
        fields_for_db.id_1c = element[7]
        fields_for_db.image_1c = element[8] if element[8] != "" else "path"
        fields_for_db.id_type_1c = element[9]
        result_list.append(fields_for_db)
    return result_list


def prepare_products_list(source_products: list, list_of_photo: list, sub_category: list) -> list:
    list_in_db = []
    actual_date = datetime.datetime.now().strftime("%x %X")
    # finding img list:
    #  print(f"source:\n{source_products[-10:]}")
    for element in source_products:
        fields_for_db = ValidateFieldsForDb()
        fields_for_db.title = "Наименование: " + element[0]
        fields_for_db.description = "Описание: " + element[1]
        fields_for_db.brand = "Roliz" if "roliz".casefold() in fields_for_db.title.casefold() else "Отсутствует"
        fields_for_db.id_1c = element[2]
        fields_for_db.id_type_1c = element[4]
        fields_for_db.sub_category_id = 0
        fields_for_db.category_id = 0
        fields_for_db.created_at = actual_date
        fields_for_db.image_url = "telegram_link"
        image_1c = element[3]
        if image_1c:
            if isinstance(image_1c, str):
                #  If one photo in line (str - format)
                #  image_1c:     "import_files/2d/2dd3b28dc16c11ea8119bcee7b8bc990_f7221e42d9f211ef815600155d025902.jpg"
                #  photo_list[i]:"13/webdata/import_files/2d/2dd3b28dc16c11ea8119bcee7b8bc990_f7221e42d9f211ef815600155d025902.jpg"
                image = ""
                for i in list_of_photo:
                    if image_1c in i:
                        image = i.strip().split("/")[-1]
                        break
                if image.strip() == "":
                    fields_for_db.image_1c = "path"
                else:
                    fields_for_db.image_1c = image
            elif isinstance(image_1c, list):
                #  If some photos in line (list[str] - format)
                image = ""
                for i in image_1c:
                    for j in list_of_photo:
                        if i in j:
                            image += j.split("/")[-1]
                            image += " "
                            break
                image_1c = image.strip()
                # print(f"image_1c = {image_1c}")
                if image_1c == "":
                    fields_for_db.image_1c = "path"
                else:
                    fields_for_db.image_1c = image_1c.strip()
        else:
            fields_for_db.image_1c = "path"
        for i in sub_category:
            if i[1] == fields_for_db.id_type_1c:
                fields_for_db.sub_category_id = i[0]
                fields_for_db.category_id = i[3]
                break
        list_in_db.append(fields_for_db)
    return list_in_db


async def updating_categories_db(source_category: list[tuple]) -> bool:
    async with moto_db:
        sub_category = await moto_db.get_all_sub_categories()
        category = await moto_db.get_categories()
    result_insert_list_category = []
    set_of_sub = set()
    for i in sub_category:
        set_of_sub.add(i[1])

    list_to_db = []

    for element in source_category:
        id_1c_sub = element[0]
        title_sub_category = element[1]

        if set_of_sub:
            if not (id_1c_sub in set_of_sub):
                result_insert_list_category.append((id_1c_sub, title_sub_category, None))
        else:
            result_insert_list_category.append((id_1c_sub, title_sub_category, None))

    for i in result_insert_list_category:
        cat = 0
        for j in category:
            sub_title = i[1]
            if sub_title.split()[0].casefold() == j[1].casefold():
                cat = j[0]
                break
            else:
                cat = 1
        list_to_db.append((i[0], i[1], cat))
    async with moto_db:
        insert_list = await moto_db.save_new_sub_category(list_to_db.copy())
        if insert_list:
            return True
        else:
            return False


async def send_photo_into_channel(list_of_photo: list) -> str | None:
    # db structure: (category_id, sub_category_id, title, brand, description, image_url, created_at, id_1c, image_1c,
    # id_type_1c)
    # list photo: ['13/webdata/import_files/00/002a592cd43411ee813c00155d025902_1f10dd56db4c11ee813c00155d025902.jpg',]
    async with moto_db:
        file_path_db = await moto_db.get_file_path_from_products_db()
    #   print(f"file_path_db:\n{file_path_db}")
    #   print(f"list_of_photo:\n{list_of_photo}")
    dict_of_photo_path = {i.split("/")[-1]: i for i in list_of_photo}
    #  print(f"dict_photo:\n{dict_of_photo_path}")
    work_list = []
    for element in file_path_db:
        for i in element[1].split():
            line = tuple()
            if i in dict_of_photo_path.keys():
                line = (element[0], dict_of_photo_path[i])
            if line:
                work_list.append(line)
    #  print(f"work list:\n{work_list}\nlen work_list = {len(work_list)}")
    await bot.send_message(chat_id=int(PRIVATE_CHAT_ID),
                           text=f"Дата обновления:\n{datetime.datetime.now().strftime("%x %X")}")
    count = 1
    now = datetime.datetime.now()
    for element in work_list:
        message = None
        try:
            message = await bot.send_photo(chat_id=int(PRIVATE_CHAT_ID),
                                           photo=types.FSInputFile(path="./xml_base/" + element[1]),
                                           caption=f"{str(element[0])} - {str(count)} шт.")
        except Exception as ex:
            print(f"Error when sending photo: {ex}")

        if message.photo[-1].file_id:
            caption = message.caption

            if caption.split()[0].isdigit():
                caption = int(caption.split()[0])

            photo_url = message.photo[-1].file_id

            async with moto_db:
                photos_urls_from_db = await moto_db.get_photo_url_from_product_id(product_id=caption)
            print(f"photos_urls_from_db = {photos_urls_from_db}")

            if photos_urls_from_db[0] != "telegram_link" and photos_urls_from_db[0] != "":
                photo_url = photos_urls_from_db[0] + " " + photo_url
            count += 1

            photo_url_data = (photo_url, caption)
            print(f"photo_url_data = {photo_url_data}")
            async with moto_db:
                await moto_db.update_photo_url_products_db(photo_url_data=photo_url_data)
        else:
            print(f"Message is Empty!")

        await asyncio.sleep(10)

    delta = datetime.datetime.now() - now
    print(f"время на отправку: {delta}")
    return "None"
