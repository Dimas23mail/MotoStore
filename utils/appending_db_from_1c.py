import asyncio
import os
import datetime
import time
from asyncio import sleep
from dataclasses import astuple

from aiogram import Bot, types

from .files_worker import make_tuples_from_xml
from .xml_parse import parse_xml
from .dict_parse import (product_group_dict_parse, products_dict_parse, storages_parse, products_in_storages_parse)
from .compare_utils import compare_tuple_lists
from config import moto_db
from storage import ValidateFieldsForDb


async def updating_db_from_xml(bot: Bot) -> str | None:
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
                                                               list_of_photo=tuples_of_new_files[0].copy(),
                                                               bot=bot)
                    #  print(f"product_list = {products_list}")
                    if products_list:
                        text = "Загрузка данных в товары прошла успешно."
                        print(text)
                        print("*" * 100)
                        #  await normalize_photo_data_in_list(list_of_photo=tuples_of_new_files[0].copy())
                        '''text = await send_photo_into_channel(tuples_of_new_files[0].copy(), bot=bot)
                        if text:
                            print(text, f"\n", "*"*100)'''

                elif "ПакетПредложений" in result_dict["КоммерческаяИнформация"].keys():
                    result_storage_list = storages_parse(result_dict)
                    result_products_in_storages = products_in_storages_parse(result_dict)

                else:
                    text = f"Проблемы с парсингом xml-файла: {i}"
                    return text
            else:
                return "Формат xml файлов не соответствует образцу!"
    else:
        return text if text else None  # "Новые файлы отсутствуют."


async def updating_storage_db():

    pass


async def updating_products_db(source_products: list[tuple], list_of_photo: list, bot: Bot) -> bool:
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
                                         field_key="id_1c", field_skip="created_at")

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

    i = await send_photo_into_channel(list_of_photo=list_of_photo, bot=bot)
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
                        image = i.strip()
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
                            image += j
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


async def send_photo_into_channel(list_of_photo: list, bot: Bot) -> str | None:
    # db structure: (category_id, sub_category_id, title, brand, description, image_url, created_at, id_1c, image_1c,
    # id_type_1c)
    # list photo: ['13/webdata/import_files/00/002a592cd43411ee813c00155d025902_1f10dd56db4c11ee813c00155d025902.jpg',]
    async with moto_db:
        file_path_db = await moto_db.get_file_path_from_products_db()
    #  print(f"file_path_db:\n{file_path_db}")
    #  print(f"list_of_photo:\n{list_of_photo}")
    work_list = []
    for element in file_path_db:
        for i in element[1].split():
            line = tuple()
            if i in list_of_photo:
                line = (element[0], i)
            if line:
                work_list.append(line)
    print(f"work list:\n{work_list}\nlen work_list = {len(work_list)}")
    await bot.send_message(chat_id=-1002227083175,
                           text=f"Дата обновления:\n{datetime.datetime.now().strftime("%x %X")}")
    count = 1
    now = datetime.datetime.now()
    for element in work_list:
        await bot.send_photo(chat_id=-1002227083175,
                             photo=types.FSInputFile(path="./xml_base/" + element[1]),
                             caption=f"{str(element[0])} - {str(count)} шт.")
        count += 1
        await asyncio.sleep(5)

    delta = datetime.datetime.now() - now
    print(f"время на отправку: {delta}")
    return "None"
