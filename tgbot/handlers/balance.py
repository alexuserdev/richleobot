from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import BalanceKeyboard
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.crypto_work import parse_balances
from tgbot.misc.db_api import UsersDb


async def main_balance(message: types.Message, state: FSMContext):
    balances = await parse_balances(message.chat.id)
    await message.answer_sticker("CAACAgIAAxkBAAICS2D1mF3tYRb7-39tdRQ_4qV6_0CwAAL_DQACo_ugSsQaq2gMY49PIAQ")
    msg = await message.answer(gen_balance_text(message, balances),
                               reply_markup=BalanceKeyboard.main())
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def join_withdraw(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Your wallet is empty")


async def show_history(call: types.CallbackQuery):
    await call.answer("No history")


def gen_balance_text(message: types.Message, balances):
    text = f"Hi {message.from_user.first_name}👋🏻👨🏻‍🔧\n\n" \
           f"Here is your balance:\n\n"
    good_balances = {}
    for wallet, sum in balances.items():
        if sum:
            good_balances[wallet] = sum
    if good_balances:
        for wallet, sum in balances.items():
            text += f"{wallet}: {round(sum, 2)}\n"
    else:
        text += "Wallet is empty\n\n"

    text += "I can help you to <b>Deposit</b> or <b>Withdraw</b> something. \n\n" \
            "If you want to perform any kind of Operation you should talk to Leo."

    return text


def register_balance(dp: Dispatcher):
    dp.register_message_handler(main_balance, text=main_menu_buttons[1], state="*")
    dp.register_callback_query_handler(join_withdraw, text="withdraw")
    dp.register_callback_query_handler(show_history, text="history")
