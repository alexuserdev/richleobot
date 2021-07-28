from random import randint

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.crypto_work import Payment
from tgbot.keyboards.inline import BalanceKeyboard
from tgbot.keyboards.reply import main_menu_buttons, BalanceKeyboardReply
from tgbot.misc.db_api import UsersDb
from tgbot.config import CryptoInformation, BinanceData
from tgbot.misc.states import DepositStates


async def deposit_join(call: types.CallbackQuery):
    await call.message.edit_text("Which currency you want to deposit",
                                 reply_markup=BalanceKeyboard.deposit_methods())
    await call.answer()


async def choosed_method(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    method = call.data.split(".")[1]
    message = call.message
    await call.message.edit_reply_markup(BalanceKeyboard.deposit_methods(method))
    if method == "NGN":
        pass
    else:
        currency = call.data.split(".")[1]
        msg = await call.message.edit_text(f"Enter amount of {currency} you want to deposit",
                                           reply_markup=BalanceKeyboard.deposit_methods(method))
        await state.update_data(currency=currency)
        await state.update_data(first_msg_id=msg.message_id)
        await DepositStates.first()
    await call.answer()


async def enter_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("currency")
    if not currency:
        return
    try:
        amount = float(message.text)
        dp = Dispatcher.get_current()
        # await dp.bot.edit_message_reply_markup(message.chat.id, data['first_msg_id'])
        await state.update_data(first_amount=amount)
        if currency == "BTC":
            payment = Payment(amount=amount + randint(10, 500) / 100000000, currency=currency)
            address = BinanceData.btc_address
        elif currency == "ETH":
            payment = Payment(amount=amount + randint(10, 500) / 10000000, currency=currency)
            address = BinanceData.eth_address
        elif currency == "USDT":
            payment = Payment(amount=amount + randint(10, 500) / 1000000, currency=currency)
            address = BinanceData.usdt_address

        payment.create()

        await message.answer(f"Send {payment.amount}{currency} on address below to deposit {currency}",
                             reply_markup=BalanceKeyboardReply.cancel())
        msg = await message.answer(address,
                                   reply_markup=BalanceKeyboard.deposit_check())
        await DepositStates.next()
        await state.update_data(payment=payment, last_msg=msg.message_id)
    except ValueError:
        await message.answer("Incorrect value")


async def approve_payment(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get("payment")
    dp = Dispatcher.get_current()
    check = await payment.check(dp)
    if check == "Success":
        await call.message.delete_reply_markup()
        await state.finish()
        await UsersDb.add_balance(call.message.chat.id, payment.currency, payment.amount)
    elif check == "Pending":
        pass
    else:
        await call.answer("Transaction not found. Please wait")


def register_deposit(dp: Dispatcher):
    dp.register_callback_query_handler(deposit_join, text="deposit")
    dp.register_callback_query_handler(choosed_method, text_contains="deposit", state=[None, DepositStates.enter_amount])
    dp.register_message_handler(enter_amount, state=DepositStates.enter_amount)
    dp.register_callback_query_handler(approve_payment, text="check", state=DepositStates.check_transaction)
