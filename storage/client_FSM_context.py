from aiogram.fsm.state import StatesGroup, State


class ClientToolsModule(StatesGroup):
    main_state_client = State()

    our_places = State()
