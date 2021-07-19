import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware


class RemoveMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            dp = Dispatcher.get_current()
            state = dp.current_state()
            datas = await state.get_data()
            await dp.bot.edit_message_reply_markup(message.chat.id, datas["last_msg"], types.ReplyKeyboardRemove())
        except:
            pass