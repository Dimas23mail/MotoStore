from aiogram.fsm.state import StatesGroup, State


class ClientToolsModule(StatesGroup):
    main_state_client = State()

    contact_info = State()
    promo_info = State()
