from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.handlers.escrow import gen_deal_text
from tgbot.handlers.start import start
from tgbot.keyboards.inline import OperationsKeyboard, ExchangeKeyboards, P2PKeyboards, EscrowKeyboards
from tgbot.keyboards.reply import main_menu_buttons, main_menu_keyboard
from tgbot.misc import binance_work
from tgbot.misc.db_api.database import UsersDb, CommissionsDb, P2PDb, EscrowDb
from tgbot.misc.states import ExchangeStates, P2PStates


async def join_p2p(call: types.CallbackQuery):
    balances = await UsersDb.parse_balance(call.message.chat.id)
    flag = False
    for k, v in balances.items():
        if v:
            flag = True
            break
    if flag:
        await call.message.edit_text("Select an action",
                                     reply_markup=P2PKeyboards.main())
    else:
        await call.message.edit_text("Wallet is empty.",
                                     reply_markup=OperationsKeyboard.deposit())
        await call.answer()


async def join_active_orders(call: types.CallbackQuery, state: FSMContext):
    orders = await P2PDb.parse_all_orders()
    if orders:
        await call.message.edit_text("Choose currency to sell",
                                     reply_markup=P2PKeyboards.p2p_active_1())
    else:
        await call.answer("No active orders now")


async def choose_first_currency_p2p(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    print("P2P")
    await call.message.edit_text("Choose currency you want to get",
                                 reply_markup=P2PKeyboards.p2p_active_2(currency=currency))
    await state.update_data(first_currency=currency)


async def choose_second_currency_p2p(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    print("p2p")
    data = await state.get_data()
    orders = await P2PDb.parse_all_orders(data['first_currency'], currency, call.message.chat.id)
    if orders:
        await call.message.delete()
        await call.message.answer("All active orders:")
        for order in orders:
            await call.message.answer(f"P2P order №{order[0]}\n"
                                      f"You give: {order[5]} {order[4]}\n" 
                                      f"You get: {order[3]} {order[2]}",
                                      reply_markup=P2PKeyboards.in_order(order[0]))
    else:
        await call.message.edit_text("No active orders now with selected params",
                                     reply_markup=None)
        await state.finish()


async def accept_p2p_deal(call: types.CallbackQuery):
    deal_id = call.data.split(".")[1]
    data, deal_id, seller_id = await P2PDb.accept_p2p_order(deal_id, call.message.chat.id)
    text = gen_deal_text(data, deal_id)
    buyer_text = gen_deal_text(data, deal_id, False)
    await call.message.delete()
    await call.message.answer("Deal successfully created",
                              reply_markup=main_menu_keyboard())
    await call.message.answer(buyer_text,
                              reply_markup=await EscrowKeyboards.in_deal(deal_id))
    dp = Dispatcher.get_current()
    await dp.bot.send_message(seller_id,
                              text,
                              reply_markup=await EscrowKeyboards.in_deal(deal_id))


async def create_order(call: types.CallbackQuery):
    await call.answer()
    text = "What do you want to give?"
    await P2PStates.first.set()
    await call.message.edit_text(text,
                                 reply_markup=P2PKeyboards.p2p_1())


async def choosed_first_wallet(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    msg = await call.message.edit_text(f"Enter amount of {currency} you want to sell",
                                       reply_markup=P2PKeyboards.p2p_1(currency))
    await state.update_data(first_currency=currency)
    await state.update_data(first_msg_id=msg.message_id)
    await call.answer()


async def enter_amount_of_first_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("first_currency")
    if not currency:
        return
    try:
        amount = float(message.text)
        msg = await message.answer("Which currency you want to get",
                                   reply_markup=P2PKeyboards.p2p_2(not_currency=currency))
        await P2PStates.next()
        dp = Dispatcher.get_current()
        await state.update_data(first_amount=amount, first_msg_id=None, second_msg_id=msg.message_id)
    except ValueError:
        await message.answer("Incorrect value")


async def choosed_second_wallet(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    data = await state.get_data()
    msg = await call.message.edit_text(f"Enter amount of {currency} you want to get",
                                       reply_markup=P2PKeyboards.p2p_2(currency,
                                                                       not_currency=data['first_currency']))
    await state.update_data(second_currency=currency)
    await call.answer()


async def enter_amount_of_second_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get("second_currency")
    if not currency:
        return
    try:
        amount = float(message.text)
        data['second_amount'] = amount
        dp = Dispatcher.get_current()
        print(data)
        await state.update_data(second_amount=amount)
        await message.answer(f"P2P order\n"
                             f"You give: {data['first_amount']} {data['first_currency']}\n" 
                             f"You'll get: {data['second_amount']} {data['second_currency']}",
                             reply_markup=P2PKeyboards.order_create_confirming())
        await P2PStates.next()
    except ValueError:
        await message.answer("Incorrect value")


async def confirm_p2p_create(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await P2PDb.create_new_order(call.message.chat.id, data['first_currency'], data['first_amount'],
                                 data['second_currency'], data['second_amount'])
    await call.message.edit_text("P2P order has been created",
                                 reply_markup=None)
    await state.finish()


async def cancel_p2p_create(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await start(call.message, state)


def register_p2p(dp: Dispatcher):
    dp.register_callback_query_handler(join_p2p, text="p2p")
    dp.register_callback_query_handler(join_active_orders, text="active_p2p_orders")
    dp.register_callback_query_handler(choose_first_currency_p2p, text_contains="to_sell_active_p2p")
    dp.register_callback_query_handler(choose_second_currency_p2p, text_contains="to_get_active_p2p")
    dp.register_callback_query_handler(accept_p2p_deal, text_contains="accept_p2p_deal")
    dp.register_callback_query_handler(create_order, text="create_p2p_order")
    dp.register_callback_query_handler(choosed_first_wallet, text_contains="to_give_p2p", state=[None,
                                                                                        P2PStates.first])
    dp.register_message_handler(enter_amount_of_first_wallet, state=P2PStates.first)
    dp.register_callback_query_handler(choosed_second_wallet, text_contains="to_get_p2p", state=P2PStates.second)
    dp.register_message_handler(enter_amount_of_second_wallet, state=P2PStates.second)
    dp.register_callback_query_handler(confirm_p2p_create, text="confirm_order_create", state=P2PStates.confirm)
    dp.register_callback_query_handler(cancel_p2p_create, text="cancel_order_create", state=P2PStates.confirm)