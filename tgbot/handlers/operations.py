import os

import qrcode
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from tgbot.keyboards.inline import OperationsKeyboard
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.db_api.database import RequestsDb, UsersDb
from tgbot.misc.states import RequestStates


async def main_operations(message: types.Message, state: FSMContext):
    await message.answer_sticker("CAACAgIAAxkBAAICVmD1mvmVX5-aB7P0jyVDHubhuuhkAAL_DQACo_ugSsQaq2gMY49PIAQ")
    msg = await message.answer("What would you like to do? 👩🏼‍🦰",
                               reply_markup=OperationsKeyboard.main())
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def join_send(call: types.CallbackQuery):
    balances = await UsersDb.parse_balance(call.message.chat.id)
    flag = False
    for k, v in balances.items():
        if v:
            flag = True
            break
    if flag:
        pass
    else:
        await call.message.edit_text("Wallet is empty.",
                                     reply_markup=OperationsKeyboard.deposit())
        await call.answer()


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
    dp.register_callback_query_handler(join_request, text="request")
    dp.register_callback_query_handler(choosed_request_method, text_contains="request", state="*")
    dp.register_message_handler(amount_entered, state=RequestStates.enter_count)
