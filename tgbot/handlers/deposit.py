from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot import config
from tgbot.keyboards.inline import BalanceKeyboard
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.db_api import UsersDb
from tgbot.config import CryptoInformation


async def deposit_join(call: types.CallbackQuery):
    await call.message.edit_text("Which currency you want to deposit",
                                 reply_markup=BalanceKeyboard.deposit_methods())
    await call.answer()


async def choosed_method(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        for msg in data['deposit_msg']:
            await Dispatcher.get_current().bot.delete_message(call.message.chat.id,
                                                              msg)
    except KeyError:
        pass
    method = call.data.split(".")[1]
    message = call.message
    await call.message.edit_reply_markup(BalanceKeyboard.deposit_methods(method))
    if method == "NGN":
        pass
    else:
        wallets = await UsersDb.parse_wallets(call.message.chat.id)
        minimum_deposit, maximum_deposit = config.CryptoInformation.deposit_amounts[method][0], "∞"
        msg = await message.answer(f"Minimum deposit amount: <b>{minimum_deposit} {method}</b>\n"
                                   f"Maximum deposit amount: <b>{maximum_deposit} {method}</b>\n"
                                   f"Fee: 0 {method}")
        msg1 = await message.answer(f"Send funds on address bellow to deposit {method}")
        if method == "BTC":
            index = 0
        elif method == "ETH":
            index = 1
        else:
            index = 2
        msg2 = await message.answer(wallets[index])
        await state.update_data(deposit_msg=[msg.message_id, msg1.message_id, msg2.message_id])
    await call.answer()


def register_deposit(dp: Dispatcher):
    dp.register_callback_query_handler(deposit_join, text="deposit")
    dp.register_callback_query_handler(choosed_method, text_contains="deposit")
