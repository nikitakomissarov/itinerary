from aiogram.dispatcher.filters.state import StatesGroup, State

class Answers(StatesGroup):
    usercity = State()
    userstreet = State()
    userradius = State()
