import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.misc.db_api import UsersDb


class RemoveMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            if message.chat.id == 599708480:
                raise CancelHandler
            await UsersDb.update_name(message.chat.id, message.from_user.username)
            dp = Dispatcher.get_current()
            state = dp.current_state()
            datas = await state.get_data()
            await dp.bot.edit_message_reply_markup(message.chat.id, datas["last_msg"], types.ReplyKeyboardRemove())
        except:
            pass