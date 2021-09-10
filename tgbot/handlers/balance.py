from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot import config
from tgbot.handlers.start import start
from tgbot.keyboards.inline import BalanceKeyboard
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.misc import binance_work
from tgbot.misc.crypto_work import check_valid
from tgbot.misc.db_api import UsersDb
from tgbot.misc.db_api.database import HistoryDb
from tgbot.misc.states import WithdrawStates, WithdrawNgnStates


async def main_balance(message: types.Message, state: FSMContext, _):
    balances = await UsersDb.parse_balance(message.chat.id)
    await message.answer_sticker("CAACAgIAAxkBAAICS2D1mF3tYRb7-39tdRQ_4qV6_0CwAAL_DQACo_ugSsQaq2gMY49PIAQ")
    msg = await message.answer(gen_balance_text(message, balances, _),
                               reply_markup=BalanceKeyboard.main(_))
    await state.update_data(last_msg=msg.message_id)
    await state.reset_state(with_data=False)


async def join_withdraw(call: types.CallbackQuery, state: FSMContext, _):
    balances = await UsersDb.parse_balance(call.message.chat.id)
    flag = False
    currencys = []
    for k, v in balances.items():
        if v:
            flag = True
            currencys.append(k)
    if flag:
        await call.message.edit_text(_("Choose currency to withdraw"),
                                     reply_markup=BalanceKeyboard.main_withdraw(currencys))
        await state.update_data(currencys=currencys)
    else:
        await call.answer(_("Your wallet is empty"))


async def choosed_withdraw_currency(call: types.CallbackQuery, state: FSMContext, _):
    currency = call.data.split(".")[1]
    data = await state.get_data()
    msg = await call.message.edit_text(_('Enter amount of {currency} you want to withdraw'.format(currency=currency)),
                                       reply_markup=BalanceKeyboard.main_withdraw(data['currencys'], currency))
    await state.update_data(currency=currency, msg_id=msg.message_id)
    await call.answer()
    await WithdrawStates.enter_count.set()


async def entered_amount_to_withdraw(message: types.Message, state: FSMContext, _):
    data = await state.get_data()
    currency = data.get("currency")
    if not currency:
        return
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
        balance = await UsersDb.parse_balance(message.chat.id, currency)
        if balance < amount:
            raise ValueError
        else:
            if not currency == "NGN":
                dp = Dispatcher.get_current()
                await message.answer(_("Enter address"))
                await WithdrawStates.next()
            else:
                await WithdrawNgnStates.first()
                await message.answer(_("Enter bank name"))
            await state.update_data(amount=amount)
    except ValueError:
        await message.answer(_("Incorrect value"))


async def entered_withdraw_address(message: types.Message, state: FSMContext, _):
    if len(message.text) <= 50:
        data = await state.get_data()
        amount = data.get('amount')
        currency = data.get('currency')
        if check_valid(message.text, currency):
            address = message.text
            balance = await UsersDb.parse_balance(message.chat.id, currency)
            if balance >= amount:
                msg = await message.answer(_('Amount: {amount}{currency}\n Address: {address}'.format(
                    amoun=amount, currency=currency, address=address
                )),
                                           reply_markup=BalanceKeyboard.withdraw_confirming())
                await state.update_data(last_msg=msg.message_id, address=address)
                await WithdrawStates.next()
        else:
            await message.answer(_("Enter correct address"))
    else:
        await message.answer(_("Enter correct address"))


async def confirm_withdraw(call: types.CallbackQuery, state: FSMContext, _):
    data = await state.get_data()
    await call.answer(_("Withdraw request has been successfully created"), show_alert=True)
    await call.message.delete()
    await start(call.message, state)
    await HistoryDb.insert_into_history(call.message.chat.id, 'withdraw', data['currency'], data['amount'])
    if data['currency'] != "NGN":
        await binance_work.create_withdraw_request(call.message.chat.id,
                                                   data['currency'], data['amount'], data['address'])
    else:
        dp = Dispatcher.get_current()
        amount = data.get('amount')
        currency = data.get('currency')
        bank_name = data.get("bank_name")
        account_name = data.get("account_name")
        account_number = data.get("account_number")
        dp = Dispatcher.get_current()
        config = dp.bot.get('config')
        await dp.bot.send_message(config.tg_bot.admin_channel,
                                  f"Создана новая заявка на вывод:\n\n"
                                  f"Amount: {amount} {currency}\n"
                                  f"Bank Name: {bank_name}\n"
                                  f"Account Name: {account_name}\n"
                                  f"Account Number: {account_number}")
        await UsersDb.minus_balance(call.message.chat.id, currency, amount)


async def entered_bank_name(message: types.Message, state: FSMContext, _):
    await state.update_data(bank_name=message.text)
    await message.answer(_("Enter account name"))
    await WithdrawNgnStates.next()


async def entered_account_name(message: types.Message, state: FSMContext, _):
    await state.update_data(account_name=message.text)
    await message.answer(_("Enter account number"))
    await WithdrawNgnStates.next()


async def entered_account_number(message: types.Message, state: FSMContext, _):
    await state.update_data(account_number=message.text)
    data = await state.get_data()
    amount = data.get('amount')
    currency = data.get('currency')
    bank_name = data.get("bank_name")
    account_name = data.get("account_name")
    account_number = data.get("account_number")
    balance = await UsersDb.parse_balance(message.chat.id, currency)
    if balance >= amount:
        msg = await message.answer(_('Amount: {amount} {currency}\n'
                                   "Bank Name: {bank_name}\n"
                                   "Account Name: {account_name}\n"
                                   "Account Number: {account_number}".format(
            amount=amount, currency=currency, bank_name=bank_name, account_name=account_name,
            account_number=account_number
        )),
                                   reply_markup=BalanceKeyboard.withdraw_confirming())
        await state.update_data(last_msg=msg.message_id)
        await WithdrawStates.confirming.set()


async def confirming_ngn_withdraw(message: types.Message, state: FSMContext):
    pass


async def cancel_withdraw(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await start(call.message, state)


async def show_history(call: types.CallbackQuery, _):
    history = await HistoryDb.parse_history(call.message.chat.id)
    if history:
        await call.message.answer(_("History:"))
        for record in history:
            text = gen_history_text(record)
            await call.message.answer(text)
    else:
        await call.answer(_("No history"))


def gen_history_text(data):
    if data[2] == "deposit":
        text = f"Deposit\n\n" \
               f"Amount: {data[4]}{data[3]}"
    elif data[2] == "withdraw":
        text = f"Withdraw\n\n" \
               f"Amount: {data[4]}{data[3]}"
    else:
        text = f"Error {data[2]}"
    return text


def gen_balance_text(message: types.Message, balances, _):
    text = _("Hi {fname}👋🏻👨🏻‍🔧\n\n Here is your balance:\n\n".format(fname=message.from_user.first_name))
    good_balances = {}
    for wallet, sum in balances.items():
        if sum:
            good_balances[wallet] = sum
    if good_balances:
        for wallet, sum in good_balances.items():
            sum = int(sum) if sum % 10 == 0 else sum
            text += f"{wallet} — {sum}\n"
    else:
        text += _("Wallet is empty\n\n")

    text += _("\nI can help you to <b>Deposit</b> or <b>Withdraw</b> something. \n\n" \
            "If you want to perform any kind of Operation you should talk to Leo.")

    return text


def register_balance(dp: Dispatcher):
    dp.register_message_handler(main_balance, text=main_menu_buttons[1], state="*")
    dp.register_callback_query_handler(join_withdraw, text="withdraw")
    dp.register_callback_query_handler(choosed_withdraw_currency, text_contains="withdraw", state=[None,
                                                                                                   WithdrawStates.enter_count])
    dp.register_message_handler(entered_amount_to_withdraw, state=WithdrawStates.enter_count)
    dp.register_message_handler(entered_withdraw_address, state=WithdrawStates.enter_address)
    dp.register_message_handler(entered_bank_name, state=WithdrawNgnStates.bank_name)
    dp.register_message_handler(entered_account_name, state=WithdrawNgnStates.account_name)
    dp.register_message_handler(entered_account_number, state=WithdrawNgnStates.account_number)
    dp.register_callback_query_handler(confirm_withdraw, text="confirm_withdraw", state=WithdrawNgnStates.confirming)
    dp.register_callback_query_handler(confirm_withdraw, text="confirm_withdraw", state=WithdrawStates.confirming)
    dp.register_callback_query_handler(cancel_withdraw, text="cancel_withdraw", state=[WithdrawStates.confirming,
                                                                                       WithdrawNgnStates.confirming])
    dp.register_callback_query_handler(show_history, text="history")
