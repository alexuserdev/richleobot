from random import randint

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.config import BinanceData, TgBot
from tgbot.handlers.start import start
from tgbot.keyboards.inline import BalanceKeyboard, AdminKeyboards
from tgbot.keyboards.reply import BalanceKeyboardReply
from tgbot.misc.crypto_work import Payment
from tgbot.misc.db_api import UsersDb
from tgbot.misc.db_api.database import AdminDb, HistoryDb
from tgbot.misc.states import DepositStates


async def main_deposit(call: types.CallbackQuery):
    await call.message.edit_text("Choose deposit method",
                                 reply_markup=BalanceKeyboard.deposit_join())
    await call.answer()

async def deposit_join(call: types.CallbackQuery):
    await call.message.edit_text("Which currency you want to deposit",
                                 reply_markup=BalanceKeyboard.deposit_methods())
    print("Deposit joined")
    await call.answer()


async def choosed_method(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    method = call.data.split(".")[1]
    print(method)
    message = call.message
    await call.message.edit_reply_markup(BalanceKeyboard.deposit_methods(method))
    if method == "NGN":
        currency = call.data.split(".")[1]
        msg = await call.message.edit_text(f"Enter amount of {currency} you want to deposit",
                                           reply_markup=BalanceKeyboard.deposit_methods(method))
        await state.update_data(currency=currency)
        await state.update_data(first_msg_id=msg.message_id)
        await DepositStates.first()
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
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
        if currency == "NGN":
            msg = await message.answer(f"To replenish your NGN account - send amount you want Bank account:\n\n"
                                       f"Account Number - 6322482013\n"
                                       f"Account Holder - HPL ALLIANCE NIGERIA LTD\n"
                                       f"Bank - FIRST CITY MONUMENT BANK (FCMB) PLC\n"
                                       f"Bank Sort Code - 214\n\n"
                                       f"Amount: {amount} NGN\n"
                                       f"Comment: leoexchange {message.chat.id}\n\n"
                                       f"🚨🚨🚨ATTENTION!🚨🚨🚨\n\n"
                                       f"It is REQUIRED to write code leoexchange {message.chat.id} in the comment section\n"
                                       f"Otherwise, deposit will not be executed",
                                       reply_markup=BalanceKeyboard.deposit_check())
            payment = Payment(amount=amount, currency="NGN")
            await DepositStates.next()
            await state.update_data(payment=payment, last_msg=msg.message_id)
        else:
            await state.update_data(first_amount=amount)
            if currency == "BTC":
                payment = Payment(amount=amount + randint(10, 500) / 100000000, currency=currency)
                address = BinanceData.btc_address
            elif currency == "ETH":
                payment = Payment(amount=amount + randint(10, 500) / 100000, currency=currency)
                address = BinanceData.eth_address
            elif currency == "USDT":
                payment = Payment(amount=amount + randint(10, 500) / 100000, currency=currency)
                address = BinanceData.usdt_address

            payment.create()

            await message.answer(f"Send {payment.amount:f}{currency} on address below to deposit {currency}",
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
    if payment.currency == "NGN":
        dp = Dispatcher.get_current()
        config = dp.bot.get('config')
        await call.answer("Wait transaction confirming")
        await call.message.delete()
        await start(call.message, state)
        id = await AdminDb.create_deposit_request(call.message.chat.id, payment.currency, payment.amount)
        await dp.bot.send_message(config.tg_bot.admin_channel,
                                  f"Новая заявка на пополненик\n\n"
                                  f"Сумма: {payment.amount}{payment.currency}\n"
                                  f"Комментарий: leoexchange {call.message.chat.id}",
                                  reply_markup=AdminKeyboards.deposit(id))
    else:
        dp = Dispatcher.get_current()
        check = await payment.check(dp)
        if check == "Success":
            await call.message.delete_reply_markup()
            await state.finish()
            await UsersDb.add_balance(call.message.chat.id, payment.currency, payment.amount)
            await call.message.edit_text("Successfully")
            await HistoryDb.insert_into_history(call.message.chat.id, 'deposit', payment.currency, payment.amount)
        elif check == "Pending":
            await call.answer("Transaction is found but not confirmed. Please wait")
        else:
            await call.answer("Transaction not found. Please wait")


def register_deposit(dp: Dispatcher):
    dp.register_callback_query_handler(main_deposit, text="deposit")
    dp.register_callback_query_handler(deposit_join, text="deposit_join")
    dp.register_callback_query_handler(choosed_method, text_contains="deposit",
                                       state=[None, DepositStates.enter_amount])
    dp.register_message_handler(enter_amount, state=DepositStates.enter_amount)
    dp.register_callback_query_handler(approve_payment, text="check", state=DepositStates.check_transaction)
