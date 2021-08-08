from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.handlers.start import start
from tgbot.keyboards.inline import OperationsKeyboard, ExchangeKeyboards
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc import binance_work
from tgbot.misc.db_api.database import UsersDb, CommissionsDb, AdminDb
from tgbot.misc.states import ExchangeStates


async def join_exchange(call: types.CallbackQuery):
    balances = await UsersDb.parse_balance(call.message.chat.id)
    flag = False
    text = "Ok, your <b>Balance</b>:\n\n\n"
    for k, v in balances.items():
        if v:
            flag = True
            text += f"{k} — {v}\n"
    if flag:
        currencys = []
        text += "\nCurrent <b>Rates</b> are:\n\n"
        dp = Dispatcher.get_current()
        for k, v in balances.items():
            if v:
                price = await binance_work.course_for_coin(dp, k)
                if price:
                    text += f"{k}\n"
                    currencys.append(k)
                try:
                    for i, j in price.items():
                        j = float(j)
                        j = j - (j / 100 * float(await CommissionsDb.parse_course_percent()))
                        text += f"1 = {float(j)} {i}\n"

                    text += "\n"
                except:
                    pass

        text += "\nWhat do you want to exchange?"

        print(currencys)

        await call.message.edit_text(text,
                                     reply_markup=ExchangeKeyboards.main_exchange(currencys))
    else:
        await call.message.edit_text("Wallet is empty.",
                                     reply_markup=OperationsKeyboard.deposit())
        await call.answer()


async def choosed_first_currency(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    await call.message.edit_text("What do you want to get",
                                 reply_markup=ExchangeKeyboards.exchange2(currency))
    await state.update_data(currency1=currency)


async def choosed_second_currency(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split(".")[1]
    data = await state.get_data()
    await call.message.edit_text(f"How much {data['currency1']} do you want to sell?")
    await ExchangeStates.first.set()
    await state.update_data(currency2=currency)


async def entered_amount(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        count = float(message.text.replace(",", "."))
        count = round(count, 10)
        if count <= await UsersDb.parse_balance(message.chat.id, data['currency1']):
            count = int(count) if count % 10 == 0 else count
            dp = Dispatcher.get_current()
            if not data['currency1'] == "NGN" and not data['currency2'] == "NGN":
                sum = await binance_work.get_pair_price(data['currency1'], data['currency2'], count, dp)
                sum = round(sum, 7)
            else:
                sum = await AdminDb.get_pair_price(data['currency1'], data['currency2'], count)
                sum = float(sum)
            sum = sum - (sum / 100 * float(await CommissionsDb.parse_exchange_commission()))
            sum = sum - (sum / 100 * float(await CommissionsDb.parse_course_percent()))
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Confirm",
                                                    callback_data="yes"))

            keyboard.add(types.InlineKeyboardButton(text="Cancel",
                                                        callback_data="no"))
            msg = await message.answer(f"You sell: {count} {data['currency1']}\n"
                                       f"You get: {sum:f} {data['currency2']}\n\n",
                                       reply_markup=keyboard)
            await state.update_data(last_msg=msg.message_id)
            await ExchangeStates.confirming.set()
        else:
            await message.answer("Invalid value")
    except ValueError:
        await message.answer("Пожалуйста, введите число")


async def accept_exchange(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    return


async def cancel_exchange(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await start(call.message, state)


def register_exchange(dp: Dispatcher):
    dp.register_callback_query_handler(join_exchange, text="exchange")
    dp.register_callback_query_handler(choosed_first_currency, text_contains="to_exchange")
    dp.register_callback_query_handler(choosed_second_currency, text_contains="to_get")
    dp.register_message_handler(entered_amount, state=ExchangeStates.first)
    dp.register_callback_query_handler(accept_exchange, text="yes", state=ExchangeStates.confirming)
    dp.register_callback_query_handler(cancel_exchange, text="no", state=ExchangeStates.confirming)
