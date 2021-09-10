from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import HelpKeyboards
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc.binance_work import get_coins_course


async def main_help(message: types.Message, state: FSMContext, _):
    await message.answer_sticker("CAACAgIAAxkBAAICSmD1l-wnns05EFPxMtEe1D-_H0spAALGDQACumaoSk8qVRdX17H8IAQ")
    msg = await message.answer(_("Official website: rich-leo.com\n\n"
                               "If you have any questions, don't hesitate asking them after clicking on '❓Ask'\n\n"
                               "Join our 👫🏼Community to discuss Leo\n\n"
                               "If you want to check what are the 🔀exchange rates or 🔢fees - click correspond buttons below"),
                               reply_markup=HelpKeyboards.main(_))
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def back_help(call: types.CallbackQuery, _):
    await call.message.edit_text(_("Official website: rich-leo.com\n\n"
                               "If you have any questions, don't hesitate asking them after clicking on '❓Ask'\n\n"
                               "Join our 👫🏼Community to discuss Leo\n\n"
                               "If you want to check what are the 🔀exchange rates or 🔢fees - click correspond buttons below"),
                                 reply_markup=HelpKeyboards.main(_))
    await call.answer()


async def exchange_rates(call: types.CallbackQuery, _):
    dp = Dispatcher.get_current()
    courses = await get_coins_course(dp)
    buy_courses = [round(i + (i / 100 * 2), 2) for i in courses]
    sell_courses = [round(i - (i / 100 * 2), 2) for i in courses]
    await call.message.edit_text(gen_exchange_info_text(buy_courses, sell_courses),
                                 reply_markup=HelpKeyboards.exchange_rates(_))
    await call.answer()


async def fees(call: types.CallbackQuery, _):
    await call.message.edit_text(_("Fees"),
                                 reply_markup=HelpKeyboards.fees(_))
    await call.answer()


def gen_exchange_info_text(buy, sell):
    text = f"📊Buy\n" \
           f"BTC: {buy[0]}NGN\n\n" \
           f"ETH: {buy[1]}NGN\n\n" \
           f"USDT: {buy[2]}NGN\n\n\n" \
           f"📊Sell\n" \
           f"BTC: {sell[0]}NGN\n\n" \
           f"ETH: {sell[1]}NGN\n\n" \
           f"USDT: {sell[2]}NGN"
    return text


def register_help(dp: Dispatcher):
    dp.register_message_handler(main_help, text=main_menu_buttons[3], state="*")
    dp.register_callback_query_handler(back_help, text="back_help")
    dp.register_callback_query_handler(exchange_rates, text="exchange_rates")
    dp.register_callback_query_handler(fees, text="fees")
