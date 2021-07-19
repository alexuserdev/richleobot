from aiogram.dispatcher.filters.state import State, StatesGroup


class FirstRegistrationStates(StatesGroup):
    first_answer = State()
    second_asnwer = State()


class RequestStates(StatesGroup):
    enter_count = State()


class EscrowStates(StatesGroup):
    first = State()
    second = State()
    enter_user_id = State()