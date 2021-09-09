from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.handlers.start import start
from tgbot.keyboards.inline import SettingsKeyboards
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.db_api import UsersDb


async def main_settings(message: types.Message, state: FSMContext, _):
    await message.answer_sticker("CAACAgIAAxkBAAICTWD1mWuhkj0O7ipXK31fBcznLt6IAAJiDgACrAipSnab1LAKNz4WIAQ")
    msg = await message.answer(_("<b>WARNING</b>: Leo is in a BETA test mode, issues may occur. \n\n"
                               "Feedback / questions: @RichLeoSupportBot\n\n"
                               "Official website: rich-leo.com"),
                               reply_markup=SettingsKeyboards.main(_))
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def back_settings(call: types.CallbackQuery, _):
    await call.message.edit_text(_("<b>WARNING</b>: Leo is in a BETA test mode, issues may occur. \n\n"
                                 "Feedback / questions: @RichLeoSupportBot \n\n"
                                 "Official website: rich-leo.com"),
                                 reply_markup=SettingsKeyboards.main())
    await call.answer()


async def change_language(call: types.CallbackQuery, _, i18n):
    print(i18n.__dir__())
    await call.message.edit_text(_("Choose language"),
                                 reply_markup=SettingsKeyboards.choose_language())
    await call.answer()


async def changed_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data.split(".")[1]
    await UsersDb.update_language(call.message.chat.id, language)
    await call.message.delete()
    await start(call.message, state)
    await state.reset_data()


def register_settings(dp: Dispatcher):
    dp.register_message_handler(main_settings, text=main_menu_buttons[2], state="*")
    dp.register_callback_query_handler(back_settings, text="back_settings")
    dp.register_callback_query_handler(change_language, text="change_language")
    dp.register_callback_query_handler(changed_language, text_contains="language")
