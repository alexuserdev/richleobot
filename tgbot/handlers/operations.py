import os

import qrcode
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from tgbot.handlers.start import start
from tgbot.keyboards.inline import OperationsKeyboard
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.db_api.database import RequestsDb, UsersDb
from tgbot.misc.states import RequestStates, SendStates


async def main_operations(message: types.Message, state: FSMContext):
    await message.answer_sticker("CAACAgIAAxkBAAICVmD1mvmVX5-aB7P0jyVDHubhuuhkAAL_DQACo_ugSsQaq2gMY49PIAQ")
    msg = await message.answer("What would you like to do? 👩🏼‍🦰",
                               reply_markup=OperationsKeyboard.main())
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def join_send(call: types.CallbackQuery, state: FSMContext):
    balances = await UsersDb.parse_balance(call.message.chat.id)
    flag = False
    currencys = []
    for k, v in balances.items():
        if v:
            flag = True
            currencys.append(k)
    if flag:
        await call.message.edit_text("Choose currency to withdraw",
                                     reply_markup=OperationsKeyboard.main_send(currencys))
        await state.update_data(currencys=currencys)
    else:
        await call.message.edit_text("Wallet is empty.",
                                     reply_markup=OperationsKeyboard.deposit())
        await call.answer()


async def choosed_currency_to_send(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    data = await state.get_data()
    msg = await call.message.edit_text(f"Enter amount of {currency} you want to withdraw",
                                       reply_markup=OperationsKeyboard.main_send(data['currencys'], currency))
    await state.update_data(currency=currency, msg_id=msg.message_id)
    await call.answer()
    await SendStates.enter_amount.set()


async def entered_amount_to_send(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("currency")
    if not currency:
        return
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
        balance = await UsersDb.parse_balance(message.chat.id, currency)
        if balance < amount:
            raise ValueError
        else:
            await message.answer("Enter user_id")
            await SendStates.next()
            await state.update_data(amount=amount)
    except ValueError:
        await message.answer("Incorrect value")


async def entered_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
        if not await UsersDb.user_exists(user_id) or user_id == message.chat.id:
            raise ValueError
        data = await state.get_data()
        amount = data.get('amount')
        currency = data.get('currency')

        balance = await UsersDb.parse_balance(message.chat.id, currency)
        if balance >= amount:
            msg = await message.answer(f"Amount: {amount}{currency}\n"
                                       f"User_id: {message.text}",
                                       reply_markup=OperationsKeyboard.send_confirming())
            await state.update_data(last_msg=msg.message_id, user_id=user_id)
            await SendStates.next()
    except ValueError:
        await message.answer("Enter correct user_id")


async def confirm_send(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer("Successfully send", show_alert=True)
    await call.message.delete()
    currency, amount, user_id = data['currency'], data['amount'], data['user_id']
    await start(call.message, state)
    await UsersDb.minus_balance(call.message.chat.id, currency, amount)
    await UsersDb.add_balance(user_id, currency, amount)
    dp = Dispatcher.get_current()
    await dp.bot.send_message(f"You got {amount}{currency} from <a href='tg://user?id={user_id}'>{user_id}</a>")


async def cancel_send(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await start(call.message, state)



async def join_request(call: types.CallbackQuery):
    await call.message.edit_text("To request funds, please specify amount and pick the currency you want to receive.\n\n",
                                 reply_markup=OperationsKeyboard.request_methods())


async def choosed_request_method(call: types.CallbackQuery, state: FSMContext):
    method = call.data.split(".")[1]
    await call.message.edit_text(f"How much {method} you want to request",
                                 reply_markup=OperationsKeyboard.request_methods(method))
    await call.answer()
    await RequestStates.enter_count.set()
    await state.update_data(method=method)


async def amount_entered(message: types.Message, state: FSMContext):
    method = (await state.get_data()).get("method")
    try:
        amount = float(message.text)
        link = await get_start_link(await RequestsDb.create_request(message.chat.id, method, amount))
        qr = qrcode.make(link)
        qr.save(f"{message.chat.id}")
        await message.answer_photo(open(f"{message.chat.id}", "rb"),
                                   f"To request {amount} {method} choose person from your contacts\n\n"
                                   f"<b>Or show them this QR.</b>")
        os.remove(f"{message.chat.id}")
        await state.finish()
    except ValueError:
        msg = await message.answer("Invalid value",
                                   reply_markup=OperationsKeyboard.request_methods(method))
        await state.update_data(last_msg=msg.message_id)


async def confirm_request(call: types.CallbackQuery):
    id = call.data.split(".")[1]
    await RequestsDb.delete_request(id)
    await call.message.edit_text("No much funds")


async def eject_request(call: types.CallbackQuery):
    id = call.data.split(".")[1]
    await RequestsDb.delete_request(id)
    await call.message.edit_text("Transaction rejected.")


def register_operations(dp: Dispatcher):
    dp.register_message_handler(main_operations, text=main_menu_buttons[0], state="*")
    dp.register_callback_query_handler(join_send, text="send")
    dp.register_callback_query_handler(choosed_currency_to_send, text_contains="send")
    dp.register_message_handler(entered_amount_to_send, state=SendStates.enter_amount)
    dp.register_message_handler(entered_user_id, state=SendStates.enter_user_id)
    dp.register_callback_query_handler(confirm_send, text="confirm_send", state=SendStates.confirming)
    dp.register_callback_query_handler(cancel_send, text="cancel_send", state=SendStates.confirming)
    dp.register_callback_query_handler(join_request, text="request")
    dp.register_callback_query_handler(choosed_request_method, text_contains="request", state="*")
    dp.register_message_handler(amount_entered, state=RequestStates.enter_count)
