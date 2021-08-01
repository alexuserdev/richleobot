from aiogram import Dispatcher, types
from aiogram.types import Message

from tgbot.misc.db_api.database import AdminDb


async def admin_start(message: Message):
    print(message.chat.id)
    await message.reply("Hello, admin!")


async def confirm_deposit(call: types.CallbackQuery):
    id = call.data.split(".")[1]
    user_id = await AdminDb.confirm_deposit_request(id)
    await call.answer("Успешно подтверждено")
    await call.message.delete()
    dp = Dispatcher.get_current()
    await dp.bot.send_message(user_id, "Your NGN deposit was confirmed")


async def cancel_deposit(call: types.CallbackQuery):
    await call.message.delete()


def register_admin(dp: Dispatcher):
    dp.register_channel_post_handler(admin_start, state="*")
    dp.register_callback_query_handler(confirm_deposit, text_contains="confirm_deposit")
    dp.register_callback_query_handler(cancel_deposit, text_contains="cancel_deposit")