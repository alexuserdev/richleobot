from aiogram.dispatcher.filters.state import State, StatesGroup


class FirstRegistrationStates(StatesGroup):
    first_answer = State()
    second_asnwer = State()


class RequestStates(StatesGroup):
    enter_count = State()


class P2PStates(StatesGroup):
    first = State()
    second = State()
    confirm = State()


class EscrowStates(StatesGroup):
    first = State()
    second = State()
    enter_user_id = State()


class ExchangeStates(StatesGroup):
    first = State()
    confirming = State()


class DepositStates(StatesGroup):
    enter_amount = State()
    check_transaction = State()


class WithdrawStates(StatesGroup):
    enter_count = State()
    enter_address = State()
    confirming = State()
