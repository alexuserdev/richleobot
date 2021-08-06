from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.start import start
from tgbot.keyboards.inline import EscrowKeyboards, OperationsKeyboard, FIAT
from tgbot.keyboards.reply import main_menu_buttons, escrow_deal_keyboard, main_menu_keyboard
from tgbot.misc import binance_work
from tgbot.misc.chat_create import create_chat
from tgbot.misc.db_api.database import RequestsDb, UsersDb, EscrowDb
from tgbot.misc.states import EscrowStates


async def cancel_deal(call: types.CallbackQuery):
    deal_id = int(call.data.split(".")[1])
    seller_id, buyer_id = await EscrowDb.delete_deal(deal_id)
    await call.message.edit_text(f"Deal №{deal_id} has been canceled")
    dp = Dispatcher.get_current()
    if call.message.chat.id == seller_id:
        user_id = buyer_id
    else:
        user_id = seller_id
    await dp.bot.send_message(user_id,
                              f"Deal №{deal_id} has been canceled")


async def accept_deal(call: types.CallbackQuery):
    deal_id = int(call.data.split(".")[1])
    try:
        res = await EscrowDb.accept_deal(call.message.chat.id, deal_id)
    except:
        await call.message.edit_text("Deal has been canceled",
                                     reply_markup=None)
        return
    if res:
        if res == "Accepted":
            await call.answer("Accepted")
            await call.message.edit_reply_markup(await EscrowKeyboards.in_deal(deal_id, 'accepted'))
        else:
            seller_id, buyer_id, id, status = res
            if status == "escrow":
                dp = Dispatcher.get_current()
                await call.message.delete()
                await dp.bot.send_message(seller_id, f"Escrow exchange №{id} was completed successfully")
                await dp.bot.send_message(buyer_id, f"Escrow exchange №{id} was completed successfully")
            else:
                dp = Dispatcher.get_current()
                await call.answer("Accepted")
                await call.message.edit_reply_markup(EscrowKeyboards.in_deal_fiat(deal_id, True))
                await dp.bot.send_message(buyer_id, f"Payment for deal №{deal_id} was reserved in the service. "
                                                    f"Please send the money")
    elif res is False:
        await call.message.answer("Wallet is empty.",
                                  reply_markup=OperationsKeyboard.deposit())
        await call.answer()
    else:
        await call.answer("Accepted")
        await call.message.edit_reply_markup(await EscrowKeyboards.in_deal(deal_id, 'accepted'))


async def accept_fiat_deal(call: types.CallbackQuery):
    deal_id = int(call.data.split(".")[1])
    res = await EscrowDb.accept_fiat_deal(deal_id)
    if res:
        seller_id, buyer_id, id = res
        dp = Dispatcher.get_current()
        await call.message.delete()
        await dp.bot.send_message(seller_id, f"Escrow exchange №{id} was completed successfully")
        await dp.bot.send_message(buyer_id, f"Escrow exchange №{id} was completed successfully")
    else:
        await call.message.answer("Wallet is empty.",
                                  reply_markup=OperationsKeyboard.deposit())
        await call.answer()


async def cancel_escrow(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dp = Dispatcher.get_current()
    try:
        if data.get('first_msg_id'):
            await dp.bot.edit_message_reply_markup(message.chat.id, data['first_msg_id'])
    except MessageNotModified:
        pass
    try:
        if data.get('second_msg_id'):
            await dp.bot.edit_message_reply_markup(message.chat.id, data['second_msg_id'])
    except MessageNotModified:
        pass
    await state.finish()
    await start(message, state)


async def escrow_exchange_join(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer_sticker("CAACAgIAAxkBAAICTGD1mJCRGvildKusT1omUJpJtl3HAAKRDQACzyCgSja8PU7hcPnqIAQ",)
    msg = await call.message.answer("Select an action",
                              reply_markup=EscrowKeyboards.main())
    await call.message.edit_reply_markup()
    await state.update_data(last_msg=msg.message_id)


async def all_active_deals(call: types.CallbackQuery):
    deals = await EscrowDb.parse_active_deals(call.message.chat.id)
    if deals:
        dp = Dispatcher.get_current()
        await call.message.edit_text("All active orders: ")
        for deal in deals:
            data = gen_data_dict(deal)
            for_seller = True if call.message.chat.id == deal[1] else False
            status = deal[-3] if for_seller else deal[-2]
            if deal[-1] == "escrow":
                text = gen_deal_text(data, deal[0], for_seller)
                rate = await binance_work.get_pair_price(data['first_currency'], data['second_currency'], 1, dp)
                text += f"\nRate: 1 {data['first_currency']} = {rate} {data['second_currency']}"
                await call.message.answer(text,
                                          reply_markup=await EscrowKeyboards.in_deal(deal[0], status))
            else:
                chat_link = await EscrowDb.parse_deal_chat(deal[0])
                text = gen_deal_text(data, deal[0], for_seller, chat_link)
                rate = await binance_work.get_pair_price(data['first_currency'], data['second_currency'], 1, dp)
                text += f"\nRate: 1 {data['first_currency']} = {rate} {data['second_currency']}"
                if for_seller:
                    if data['first_currency'] in FIAT:
                        keyboard = EscrowKeyboards.in_deal_fiat(deal[0], "fiat")
                    else:
                        keyboard = EscrowKeyboards.in_deal_fiat(deal[0], status)
                else:
                    if data['first_currency'] in FIAT:
                        keyboard = EscrowKeyboards.in_deal_fiat(deal[0], status)
                    else:
                        keyboard = EscrowKeyboards.in_deal_fiat(deal[0], "fiat")
                await call.message.answer(text,
                                          reply_markup=keyboard)
    else:
        await call.answer("You don't have active deals")


async def escrow_create(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Escrow exchange",
                              reply_markup=escrow_deal_keyboard())
    await call.message.answer("Which currency you want to sell",
                              reply_markup=EscrowKeyboards.choose_currency())
    await EscrowStates.first.set()


async def choosed_first_wallet(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    msg = await call.message.edit_text(f"Enter amount of {currency} you want to sell",
                                       reply_markup=EscrowKeyboards.choose_currency(currency))
    await state.update_data(first_currency=currency)
    await state.update_data(first_msg_id=msg.message_id)
    await call.answer()


async def enter_amount_of_first_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("first_currency")
    if not currency:
        return
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
        msg = await message.answer("Which currency you want to get",
                                   reply_markup=EscrowKeyboards.choose_currency(not_currency=currency))
        await EscrowStates.next()
        dp = Dispatcher.get_current()
        await dp.bot.edit_message_reply_markup(message.chat.id, data['first_msg_id'])
        await state.update_data(first_amount=amount, first_msg_id=None, second_msg_id=msg.message_id)
    except ValueError:
        await message.answer("Incorrect value")


async def choosed_second_wallet(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    data = await state.get_data()
    msg = await call.message.edit_text(f"Enter amount of {currency} you want to get",
                                       reply_markup=EscrowKeyboards.choose_currency(currency,
                                                                                    not_currency=data['first_currency']))
    await state.update_data(second_currency=currency)
    await call.answer()


async def enter_amount_of_second_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("second_currency")
    if not currency:
        return
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
        await message.answer("Enter username or ID of second transaction participant")
        await EscrowStates.next()
        dp = Dispatcher.get_current()
        await dp.bot.edit_message_reply_markup(message.chat.id, data['second_msg_id'])
        await state.update_data(second_amount=amount)
    except ValueError:
        await message.answer("Incorrect value")


async def enter_user_id(message: types.Message, state: FSMContext):
    try:
        try:
            user_id = int(message.text)
        except ValueError:
            user_id = message.text
            user_id = user_id if not user_id[0] == "@" else user_id[1:]
            user_id = await UsersDb.parse_user_id(user_id)
        if not await UsersDb.user_exists(user_id) or user_id == message.chat.id:
            raise ValueError
        dp = Dispatcher.get_current()
        data = await state.get_data()
        data['seller_id'] = message.chat.id
        data['buyer_id'] = user_id
        deal_id, status = await EscrowDb.create_deal(data, "escrow")
        if status == 'escrow':
            text, buyer_text = gen_deal_text(data, deal_id), gen_deal_text(data, deal_id, False)
            rate = await binance_work.get_pair_price(data['first_currency'], data['second_currency'], 1, dp)
            text += f"\nRate: 1 {data['first_currency']} = {rate:f} {data['second_currency']}"
            buyer_text += f"\nRate: 1 {data['first_currency']} = {rate:} {data['second_currency']}"
            await message.answer("Deal successfully created",
                                 reply_markup=main_menu_keyboard())
            await message.answer(text,
                                 reply_markup=await EscrowKeyboards.in_deal(deal_id))
            await dp.bot.send_message(user_id,
                                      buyer_text,
                                      reply_markup=await EscrowKeyboards.in_deal(deal_id))
            await state.finish()
        else:
            chat_link, chat_id = await create_chat(deal_id)
            text, buyer_text = gen_deal_text(data, deal_id, chat_link=chat_link), \
                               gen_deal_text(data, deal_id, False, chat_link=chat_link)
            await message.answer("Deal successfully created",
                                 reply_markup=main_menu_keyboard())
            rate = await binance_work.get_pair_price(data['first_currency'], data['second_currency'], 1, dp)
            text += f"\nRate: 1 {data['first_currency']} = {rate:f} {data['second_currency']}"
            buyer_text += f"\nRate: 1 {data['first_currency']} = {rate:f} {data['second_currency']}"
            await message.answer(text,
                                 reply_markup=await EscrowKeyboards.in_deal(deal_id))
            await dp.bot.send_message(user_id,
                                      buyer_text)
            await state.finish()
    except ValueError:
        await message.answer("Incorrect value or user not registered in bot")


def gen_data_dict(info):
    data = {}
    data["seller_id"] = info[1]
    data["buyer_id"] = info[2]
    data["first_currency"] = info[3]
    data["first_amount"] = info[4]
    data["second_currency"] = info[5]
    data["second_amount"] = info[6]
    return data


def gen_deal_text(info, deal_id, for_seller=True, chat_link=None):
    if for_seller:
        text = f"Deal №{deal_id} with <a href='tg://user?id={info['buyer_id']}'>{info['buyer_id']}</a>\n\n" \
               f"You give: {info['first_amount']} {info['first_currency']}\n" \
               f"You'll get: {info['second_amount']} {info['second_currency']}"
    else:
        text = f"Deal №{deal_id} with <a href='tg://user?id={info['seller_id']}'>{info['seller_id']}</a>\n\n" \
               f"You give: {info['second_amount']} {info['second_currency']}\n" \
               f"You'll get: {info['first_amount']} {info['first_currency']}"
    if chat_link:
        text += f"\n\nChat: {chat_link}"
    return text


def register_escrow(dp: Dispatcher):
    dp.register_message_handler(cancel_escrow, text="Cancel", state="*")
    dp.register_callback_query_handler(escrow_exchange_join, text="escrow")
    dp.register_callback_query_handler(escrow_create, text="create_escrow_deal")
    dp.register_callback_query_handler(all_active_deals, text="my_active_escrow")
    dp.register_callback_query_handler(accept_deal, text_contains="accept_deal")
    dp.register_callback_query_handler(accept_fiat_deal, text_contains="accept_fiat_deal")
    dp.register_callback_query_handler(cancel_deal, text_contains="cancel_deal")
    dp.register_callback_query_handler(choosed_first_wallet, text_contains="currency", state=EscrowStates.first)
    dp.register_message_handler(enter_amount_of_first_wallet, state=EscrowStates.first)
    dp.register_callback_query_handler(choosed_second_wallet, text_contains="currency", state=EscrowStates.second)
    dp.register_message_handler(enter_amount_of_second_wallet, state=EscrowStates.second)
    dp.register_message_handler(enter_user_id, state=EscrowStates.enter_user_id)