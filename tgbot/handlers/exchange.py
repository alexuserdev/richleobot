from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.handlers.start import start
from tgbot.keyboards.inline import OperationsKeyboard, ExchangeKeyboards
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc import binance_work
from tgbot.misc.db_api.database import UsersDb, CommissionsDb, AdminDb
from tgbot.misc.states import ExchangeStates


async def join_exchange(call: types.CallbackQuery, _):
    balances = await UsersDb.parse_balance(call.message.chat.id)
    flag = False
    text = _("Ok, your <b>Balance</b>:\n\n\n")
    for k, v in balances.items():
        if v:
            flag = True
            text += f"{k} — {v}\n"
    if flag:
        currencys = []
        text += _("\nCurrent <b>Rates</b> are:\n\n")
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
                        j = round(j, 3) if j > 1 else j
                        if j > 1:
                            text += f'1 = {j} {i}\n'
                        else:
                            text += f'1 = {("%.17f" % j).rstrip("0").rstrip(".")} {i}\n'
                    text += "\n"
                except:
                    pass

        text += _("\nWhat do you want to exchange?")

        print(currencys)

        await call.message.edit_text(text,
                                     reply_markup=ExchangeKeyboards.main_exchange(currencys))
    else:
        await call.message.edit_text(_("Wallet is empty."),
                                     reply_markup=OperationsKeyboard.deposit())
        await call.answer()


async def choosed_first_currency(call: types.CallbackQuery, state: FSMContext, _):
    currency = call.data.split(".")[1]
    await call.message.edit_text(_("What do you want to get"),
                                 reply_markup=ExchangeKeyboards.exchange2(currency))
    await state.update_data(currency1=currency)


async def choosed_second_currency(call: types.CallbackQuery, state: FSMContext, _):
    currency = call.data.split(".")[1]
    data = await state.get_data()
    await call.message.edit_text(_("How much {data['currency1']} do you want to sell?".format(data=data)))
    await ExchangeStates.first.set()
    await state.update_data(currency2=currency)


async def entered_amount(message: types.Message, state: FSMContext, _):
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
            sum = round(sum, 3) if sum > 1 else sum
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text=_("Confirm"),
                                                    callback_data="yes"))
            await state.update_data(count=count, sum=sum)
            keyboard.add(types.InlineKeyboardButton(text="Cancel",
                                                        callback_data="no"))
            msg = await message.answer(_("You sell: {count} {data['currency1']}\n You get: {sum:f} {data['currency2']}\n\n".format(
                sum=sum, data=data, count=count
            )),
                                       reply_markup=keyboard)
            await state.update_data(last_msg=msg.message_id)
            await ExchangeStates.confirming.set()
        else:
            await message.answer(_("Invalid value"))
    except ValueError:
        await message.answer(_("Please, enter num"))


async def accept_exchange(call: types.CallbackQuery, state: FSMContext, _):
    await call.answer()
    data = await state.get_data()
    first_currency = data.get('currency1')
    second_currency = data.get('currency2')
    count = data.get('count')
    sum = data.get('sum')
    if first_currency != "NGN" or second_currency != "NGN":
        await binance_work.make_exchange(first_currency, second_currency, count)
    await UsersDb.minus_balance(call.message.chat.id, first_currency, count)
    await UsersDb.add_balance(call.message.chat.id, second_currency, sum)
    await call.message.edit_text(_("Successfully exchanged"))
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
