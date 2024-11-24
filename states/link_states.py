from aiogram.fsm.state import StatesGroup, State

class LinkStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_title = State()
    waiting_for_category = State()
    waiting_for_source = State()
    waiting_for_priority = State()