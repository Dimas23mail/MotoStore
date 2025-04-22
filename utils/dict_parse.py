#  Разбираем группы товаров из import0_1.xml
def product_group_dict_parse(source: dict) -> list[tuple]:
    product_groups = []
    tmp = source["КоммерческаяИнформация"]["Классификатор"]["Группы"]["Группа"]
    for element in tmp:
        if "Группы" in element.keys():
            groups_list = (element["Группы"]["Группа"])
            for line in groups_list:
                if line["Ид"] and line["Наименование"]:
                    product_groups.append((line["Ид"], line["Наименование"]))
        else:
            if element["Ид"] and element["Наименование"]:
                product_groups.append((element["Ид"], element["Наименование"]))

    return product_groups.copy()


#  Разбираем список товаров из import0_1.xml
def products_dict_parse(source: dict) -> list[tuple]:
    #  products_list = [("title", "description", "id_1c", "image_1c", "id_type_1c"),]
    products_list = []
    tmp = source["КоммерческаяИнформация"]["Каталог"]["Товары"]["Товар"]
    for i in tmp:
        id_1c = i["Ид"]
        title = i["Наименование"]
        description = i["ЗначенияРеквизитов"]["ЗначениеРеквизита"][-1]["Значение"]
        if "Картинка" in i.keys():
            image_1c = i["Картинка"]
        else:
            image_1c = ""
        id_type_1c = i["Группы"]["Ид"]
        products_list.append((title, description, id_1c, image_1c, id_type_1c))

    return products_list.copy()


#  Разбираем склады из offers0_1.xml
def storages_parse(source: dict) -> list[tuple]:
    #  storages_list = [("id_1c", "title", "address"), ]
    storages_list = []
    tmp = source["КоммерческаяИнформация"]["ПакетПредложений"]["Склады"]["Склад"]
    for i in tmp:
        id_1c = i["Ид"]
        title = i["Наименование"]
        if "Адрес" in i.keys():
            address = i["Контакты"]["Контакт"]["Значение"]
        else:
            address = None
        storages_list.append((id_1c, title, address))
    return storages_list.copy()


#  Разбираем количество товаров на складах из offers0_1.xml
def products_in_storages_parse(source: dict) -> list[tuple]:
    #  storages_list = [("id_product_1c", "id_storage_1c", "quantity", "price_for_pce"), ]
    storages_list = []
    tmp = source["КоммерческаяИнформация"]["ПакетПредложений"]["Предложения"]["Предложение"]
    for i in tmp:
        id_product_1c = i["Ид"]
        price_for_pce = i["Цены"]["Цена"]["ЦенаЗаЕдиницу"]
        quantity = None
        id_storage_1c = None
        for j in i["Склад"]:
            if j["КоличествоНаСкладе"] != "0":
                quantity = j["КоличествоНаСкладе"]
                id_storage_1c = j["ИдСклада"]
                storages_list.append((id_product_1c, id_storage_1c, quantity, price_for_pce))
        if quantity is None:
            storages_list.append((id_product_1c, id_storage_1c, quantity, price_for_pce))
    return storages_list.copy()
