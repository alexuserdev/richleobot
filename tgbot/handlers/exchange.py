from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import OperationsKeyboard
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.crypto_work import parse_balances


async def main_operations(message: types.Message, state: FSMContext):
    msg = await message.answer("operations",
                               reply_markup=OperationsKeyboard.main())
    await state.update_data(last_msg=msg.message_id)


async def join_send(call: types.CallbackQuery):
    balances = await parse_balances(call.message.chat.id)


def register_operations(dp: Dispatcher):
    dp.register_message_handler(main_operations, text=main_menu_buttons[0])
