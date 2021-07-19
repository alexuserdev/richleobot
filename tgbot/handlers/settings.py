from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.handlers.start import start
from tgbot.keyboards.inline import SettingsKeyboards
from tgbot.keyboards.reply import main_menu_buttons


async def main_settings(message: types.Message, state: FSMContext):
    await message.answer_sticker("CAACAgIAAxkBAAICTWD1mWuhkj0O7ipXK31fBcznLt6IAAJiDgACrAipSnab1LAKNz4WIAQ")
    msg = await message.answer("<b>WARNING</b>: Leo is in a BETA test mode, issues may occur. \n\n"
                               "Feedback / questions: @alicebobhelp \n\n"
                               "Official website: www.leo.exchange",
                               reply_markup=SettingsKeyboards.main())
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def back_settings(call: types.CallbackQuery):
    await call.message.edit_text("<b>WARNING</b>: Leo is in a BETA test mode, issues may occur. \n\n"
                                 "Feedback / questions: @alicebobhelp \n\n"
                                 "Official website: www.leo.exchange",
                                 reply_markup=SettingsKeyboards.main())
    await call.answer()


async def change_language(call: types.CallbackQuery):
    await call.message.edit_text("Choose language",
                                 reply_markup=SettingsKeyboards.choose_language())
    await call.answer()


async def changed_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data.split(".")[1]
    await call.message.delete()
    await start(call.message, state)
    await state.reset_data()


def register_settings(dp: Dispatcher):
    dp.register_message_handler(main_settings, text=main_menu_buttons[2], state="*")
    dp.register_callback_query_handler(back_settings, text="back_settings")
    dp.register_callback_query_handler(change_language, text="change_language")
    dp.register_callback_query_handler(changed_language, text_contains="language")
