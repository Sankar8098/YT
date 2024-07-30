from aiogram.fsm.state import StatesGroup, State


class SendMessages(StatesGroup):
    message = State()
    confirm = State()
