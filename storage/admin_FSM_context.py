from aiogram.fsm.state import StatesGroup, State


class AdminToolsModule(StatesGroup):
    main_state_admin = State()
    main_menu_admin = State()

    change_products_menu = State()
    adding_products = State()

    change_category_menu = State()
    adding_category = State()
    deleting_category = State()

    change_spare_types_menu = State()
    adding_spare_types = State()
    deleting_spare_types = State()

    change_promo_menu = State()

    adding_promo = State()
    adding_promo_description = State()

    deleting_promo = State()
    testing_promo_code = State()

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

    contact_info = State()

    promo_info = State()
