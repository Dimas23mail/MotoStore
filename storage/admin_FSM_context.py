from aiogram.fsm.state import StatesGroup, State


class AdminToolsModule(StatesGroup):
    main_state_admin = State()
    main_menu_admin = State()

    change_products_menu = State()
    adding_products = State()

    change_promo_menu = State()

    change_contact_menu = State()

    change_contact_main = State()
    change_contact_title = State()
    change_contact_city = State()
    change_contact_address = State()
    change_contact_phone = State()

    adding_contact_title = State()
    adding_contact_city = State()
    adding_contact_address = State()
    adding_contact_phone = State()

    delete_contact_main = State()

    change_category_menu = State()
    adding_category = State()
    deleting_category = State()

    change_place_menu = State()
    start_change_place = State()
    change_place_name = State()
    change_place_description = State()
    change_place_city = State()
    change_place_address = State()
    change_place_telephone = State()
    change_place_photo = State()

    adding_place = State()
    input_place_name = State()
    input_place_description = State()
    input_place_city = State()
    input_place_address = State()
    input_place_telephone = State()
    input_place_pictures = State()
    result_new_place_information = State()
    send_again = State()

    deleting_place = State()

