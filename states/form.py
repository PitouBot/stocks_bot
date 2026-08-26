from aiogram.fsm.state import State, StatesGroup

class AddStock(StatesGroup):
    waiting_for_ticker = State()