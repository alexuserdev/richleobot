from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import EscrowKeyboards
from tgbot.keyboards.reply import main_menu_buttons, escrow_deal_keyboard
from tgbot.misc.crypto_work import parse_balances
from tgbot.misc.db_api.database import RequestsDb, UsersDb, EscrowDb
from tgbot.misc.states import EscrowStates


async def cancel_escrow(message: types.Message):
    pass


async def escrow_exchange_join(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer_sticker("CAACAgIAAxkBAAICTGD1mJCRGvildKusT1omUJpJtl3HAAKRDQACzyCgSja8PU7hcPnqIAQ",
                                      reply_markup=escrow_deal_keyboard())
    await call.message.answer("Which currency you want to sell",
                              reply_markup=EscrowKeyboards.choose_currency())
    await EscrowStates.first()


async def choosed_first_wallet(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    msg = await call.message.edit_text(f"Enter amount of {currency} ypu want to sell",
                                       reply_markup=EscrowKeyboards.choose_currency(currency))
    await state.update_data(first_currency=currency)
    await state.update_data(first_msg_id=msg.message_id)


async def enter_amount_of_first_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("first_currency")
    if currency:
        return
    try:
        amount = float(message.text)
        await message.answer("Which currency you want to get",
                             reply_markup=EscrowKeyboards.choose_currency())
        await EscrowStates.next()
        dp = Dispatcher.get_current()
        await dp.bot.edit_message_reply_markup(message.chat.id, data['first_msg_id'])
        await state.update_data(first_amount=amount)
    except ValueError:
        await message.answer("Incorrect value")


async def choosed_second_wallet(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    msg = await call.message.edit_text(f"Enter amount of {currency} ypu want to get",
                                       reply_markup=EscrowKeyboards.choose_currency(currency))
    await state.update_data(second_currency=currency)
    await state.update_data(second_msg_id=msg.message_id)


async def enter_amount_of_second_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("second_currency")
    if currency:
        return
    try:
        amount = float(message.text)
        await message.answer("Enter ID of second transaction participants")
        await EscrowStates.next()
        dp = Dispatcher.get_current()
        await dp.bot.edit_message_reply_markup(message.chat.id, data['second_msg_id'])
        await state.update_data(second_amount=amount)
    except ValueError:
        await message.answer("Incorrect value")


async def enter_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
        if not await UsersDb.user_exists(user_id):
            raise ValueError
        data = await state.get_data()
        data['seller_id'] = message.chat.id
        data['buyer_id'] = user_id
        deal_id = await EscrowDb.create_deal(data)
        text, buyer_text = gen_deal_text(data), gen_deal_text(data, False)
        await message.answer(text,
                             reply_markup=EscrowKeyboards.in_deal(deal_id))

    except ValueError:
        await message.answer("Incorrect value or user not registered in bot")


def gen_deal_text(info, for_seller=True):
    if for_seller:
        text = f"Deal with <a href='tg://user?id={info['buyer_id']}'>{info['buyer_id']}</a>\n\n" \
               f"You give: {info['first_amount']} {info['first_currency']}\n" \
               f"You'll get: {info['second_amount']} {info['second_currency']}"
    else:
        text = f"Deal with <a href='tg://user?id={info['seller_id']}'>{info['seller_id']}</a>\n\n" \
               f"You give: {info['second_amount']} {info['second_currency']}\n" \
               f"You'll get: {info['first_amount']} {info['first_currency']}"
    return text


def register_escrow(dp: Dispatcher):
    dp.register_message_handler(cancel_escrow, text="Cancel", state="*")
    dp.register_callback_query_handler(escrow_exchange_join, text="escrow")
    dp.register_callback_query_handler(choosed_first_wallet, text_contains="currency", state=EscrowStates.first)
    dp.register_message_handler(enter_amount_of_first_wallet, state=EscrowStates.first)
    dp.register_callback_query_handler(choosed_second_wallet, text_contains="currency", state=EscrowStates.first)
    dp.register_message_handler(enter_amount_of_second_wallet, state=EscrowStates.first)
    dp.register_message_handler(enter_user_id, state=EscrowStates.enter_user_id)