from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import OperationsKeyboard, ExchangeKeyboards
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc import binance_work
from tgbot.misc.db_api.database import UsersDb
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
                currencys.append(k)
                price = await binance_work.course_for_coin(dp, k)
                text += f"{k}\n"
                for i, j in price.items():
                    text += f"1 = {float(j)} {i}\n"

                text += "\n"

        text += "\nWhat do you want to exchange?"

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
        count = float(message.text)
        count = round(count, 10)
        count = int(count) if count % 10 == 0 else count
        sum = binance_test.get_pair_price(data['vallet1'], data['vallet2'], count)
        sum = round(sum, 7)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Да",
                                                callback_data="yes"))

        keyboard.add(types.InlineKeyboardButton(text="Нет",
                                                callback_data="no"))
        await message.answer(f"За продажу {count}{data['vallet1']} вы получите {sum}{data['vallet2']}\n\n"
                             f"Вы согласны?",
                             reply_markup=keyboard)
        await ExchangeStates.confirming.set()
    except ValueError:
        await message.answer("Пожалуйста, введите число")



def register_exchange(dp: Dispatcher):
    dp.register_callback_query_handler(join_exchange, text="exchange")
    dp.register_callback_query_handler(choosed_first_currency, text_containt="to_exchange")
    dp.register_callback_query_handler(choosed_second_currency, text_contains="to_get")
    dp.register_message_handler(entered_amount, state=ExchangeStates.first)
