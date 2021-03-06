from aiogram import types

CRYPTOS = ["BTC", "ETH", "USDT"]
FIAT = ["NGN"]
WALLETS = ["BTC", "ETH", "USDT", "NGN"]
DEPOSIT_WALLETS = ["BTC(BTC)", "ETH(ERC20)", "USDT(TRC20)", "NGN (Bank Transfer)"]


class P2PKeyboards:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Active orders",
                                                callback_data="active_p2p_orders"))
        keyboard.add(types.InlineKeyboardButton(text="Create order",
                                                callback_data="create_p2p_order"))
        keyboard.add(types.InlineKeyboardButton(text="My orders",
                                                callback_data="my_p2p_orders"))
        return keyboard

    @staticmethod
    def manage_order(order_id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Delete",
                                                callback_data=f"delete_p2p_deal.{order_id}"))
        return keyboard

    @staticmethod
    def p2p_active_1():
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                       callback_data=f"to_sell_active_p2p.{wallet}"))
        return keyboard

    @staticmethod
    def p2p_active_2(currency):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        if currency in FIAT:
            lst = CRYPTOS
        else:
            lst = FIAT
        for wallet in lst:
           keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                       callback_data=f"to_get_active_p2p.{wallet}"))
        return keyboard

    @staticmethod
    def in_order(order_id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Accept",
                                                callback_data=f"accept_p2p_deal.{order_id}"))
        return keyboard

    @staticmethod
    def p2p_1(currency=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if wallet == currency:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{wallet}",
                                                           callback_data=f"to_give_p2p.{wallet}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                           callback_data=f"to_give_p2p.{wallet}"))
        return keyboard

    @staticmethod
    def p2p_2(currency=None, not_currency=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        if not_currency in FIAT:
            lst = CRYPTOS
        else:
            lst = FIAT
        for wallet in lst:
            if currency == wallet:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{wallet}",
                                                           callback_data=f"to_get_p2p.{wallet}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                           callback_data=f"to_get_p2p.{wallet}"))
        return keyboard

    @staticmethod
    def order_create_confirming():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Create",
                                                callback_data="confirm_order_create"))
        keyboard.add(types.InlineKeyboardButton(text="Cancel",
                                                callback_data="cancel_order_create"))
        return keyboard


class ExchangeKeyboards:
    @staticmethod
    def main_exchange(currencys, choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for currency in currencys:
            if choose == currency:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{currency}",
                                                           callback_data=f"to_exchange.{currency}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=currency,
                                                           callback_data=f"to_exchange.{currency}"))
        return keyboard

    @staticmethod
    def exchange2(currency):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if wallet != currency:
                keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                           callback_data=f"to_get.{wallet}"))
        print(keyboard)
        return keyboard


class OperationsKeyboard:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton(text="????Deposit",
                                                   callback_data="deposit"))
        keyboard.insert(types.InlineKeyboardButton(text="????Withdraw",
                                                   callback_data="withdraw"))
        keyboard.insert(types.InlineKeyboardButton(text="????Fast exchange",
                                                callback_data="exchange"))
        keyboard.insert(types.InlineKeyboardButton(text="????Escrow exchange",
                                                   callback_data="escrow"))
        keyboard.add(types.InlineKeyboardButton(text="????P2P",
                                                callback_data="p2p"))
        return keyboard

    @staticmethod
    def deposit():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="????Deposit",
                                                callback_data="deposit"))
        return keyboard

    @staticmethod
    def request_methods(choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if choose == wallet:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{wallet}",
                                                           callback_data=f"request.{wallet}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                           callback_data=f"request.{wallet}"))
        print(keyboard)
        return keyboard

    @staticmethod
    def in_request(id):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton(text="Reject",
                                                   callback_data=f"reject.{id}"))
        keyboard.insert(types.InlineKeyboardButton(text="Confirm",
                                                  callback_data=f"confirm.{id}"))
        return keyboard

    @staticmethod
    def main_send(currencys, choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for currency in currencys:
            if choose == currency:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{currency}",
                                                           callback_data=f"send.{currency}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=currency,
                                                           callback_data=f"send.{currency}"))
        return keyboard

    @staticmethod
    def send_confirming():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Confirm",
                                                callback_data="confirm_send"))
        keyboard.add(types.InlineKeyboardButton(text="Cancel",
                                                callback_data="cancel_send"))
        return keyboard


class BalanceKeyboard:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton(text="????Deposit",
                                                   callback_data="deposit"))
        keyboard.insert(types.InlineKeyboardButton(text="????Withdraw",
                                                   callback_data="withdraw"))
        keyboard.add(types.InlineKeyboardButton(text="????Send",
                                                callback_data="send"))
        keyboard.insert(types.InlineKeyboardButton(text="????History",
                                                   callback_data="history"))
        return keyboard

    @staticmethod
    def deposit_join():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.insert(types.InlineKeyboardButton(text="????Deposit",
                                                   callback_data="deposit_join"))
        keyboard.insert(types.InlineKeyboardButton(text="????Request",
                                                   callback_data="request"))
        return keyboard

    @staticmethod
    def deposit_methods(choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for i in range(len(WALLETS)):
            wallet = WALLETS[i]
            if choose == wallet:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{DEPOSIT_WALLETS[i]}",
                                                           callback_data=f"deposit.{wallet}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=DEPOSIT_WALLETS[i],
                                                           callback_data=f"deposit.{wallet}"))
        return keyboard

    @staticmethod
    def deposit_check():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Check",
                                                callback_data="check"))
        return keyboard

    @staticmethod
    def main_withdraw(currencys, choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for currency in currencys:
            currency_text = BalanceKeyboard.conv_currency(currency)
            if choose == currency:
                keyboard.insert(types.InlineKeyboardButton(text=f"???{currency_text}",
                                                           callback_data=f"withdraw.{currency}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=currency_text,
                                                           callback_data=f"withdraw.{currency}"))
        return keyboard

    @staticmethod
    def conv_currency(currency):
        if currency == "BTC":
            plus = "(BTC)"
        elif currency == "ETH":
            plus = "(ERC20)"
        elif currency == "USDT":
            plus = "(TRC20)"
        elif currency == "NGN":
            plus = " (Bank Transfer)"
        return currency + plus

    @staticmethod
    def withdraw_confirming():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Confirm",
                                                callback_data="confirm_withdraw"))
        keyboard.add(types.InlineKeyboardButton(text="Cancel",
                                                callback_data="cancel_withdraw"))
        return keyboard


class SettingsKeyboards:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="????Language",
                                                   callback_data="change_language"))
        keyboard.insert(types.InlineKeyboardButton(text="Privacy policy",
                                                   callback_data="d"))
        keyboard.insert(types.InlineKeyboardButton(text="Term of use",
                                                   callback_data="fds"))

        return keyboard

    @staticmethod
    def choose_language():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="????????English",
                                                   callback_data="language.END"))
        keyboard.insert(types.InlineKeyboardButton(text="????Back",
                                                   callback_data="back_settings"))
        return keyboard


class HelpKeyboards:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton(text="???Ask",
                                                   url="https://t.me/RichLeoSupportBot"))
        keyboard.insert(types.InlineKeyboardButton(text="????Exchange rates",
                                                   callback_data="exchange_rates"))
        keyboard.insert(types.InlineKeyboardButton(text="????Community",
                                                   url="https://t.me/joinchat/jvqdlHctpMZkNTgy"))
        keyboard.insert(types.InlineKeyboardButton(text="????Fees",
                                                   callback_data="fees"))
        return keyboard

    @staticmethod
    def exchange_rates():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="????Exchange",
                                                   callback_data="exchange"))
        keyboard.insert(types.InlineKeyboardButton(text="????Back",
                                                   callback_data="back_help"))
        return keyboard

    @staticmethod
    def fees():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="????Back",
                                                   callback_data="back_help"))
        return keyboard


class EscrowKeyboards:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text="Create deal",
                                                callback_data="create_escrow_deal"))
        keyboard.add(types.InlineKeyboardButton(text="Active deals",
                                                callback_data="my_active_escrow"))
        return keyboard

    @staticmethod
    def choose_currency(currency=None, not_currency=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if wallet != not_currency:
                if currency == wallet:
                    keyboard.insert(types.InlineKeyboardButton(text=f"???{wallet}",
                                                               callback_data=f"currency.{wallet}"))
                else:
                    keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                               callback_data=f"currency.{wallet}"))
        return keyboard

    @staticmethod
    async def in_deal(deal_id, status=None):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if status:
            keyboard.add(types.InlineKeyboardButton(text="Cancel deal",
                                                    callback_data=f"cancel_deal.{deal_id}"))
            return keyboard
        keyboard.add(types.InlineKeyboardButton(text="Accept",
                                                callback_data=f"accept_deal.{deal_id}"))
        keyboard.add(types.InlineKeyboardButton(text="Cancel deal",
                                                callback_data=f"cancel_deal.{deal_id}"))
        return keyboard

    @staticmethod
    def in_deal_fiat(deal_id, status=None):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if status is True:
            keyboard.add(types.InlineKeyboardButton(text="Confirm receipt",
                                                    callback_data=f"accept_fiat_deal.{deal_id}"))
            keyboard.add(types.InlineKeyboardButton(text="Cancel deal",
                                                    callback_data=f"cancel_deal.{deal_id}"))
            return keyboard
        keyboard.add(types.InlineKeyboardButton(text="Accept",
                                                callback_data=f"accept_deal.{deal_id}"))
        keyboard.add(types.InlineKeyboardButton(text="Cancel deal",
                                                callback_data=f"cancel_deal.{deal_id}"))
        return keyboard


class AdminKeyboards:
    @staticmethod
    def deposit(id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="??????????????????????",
                                                callback_data=f"confirm_deposit.{id}"))
        keyboard.add(types.InlineKeyboardButton(text="??????????????????",
                                                callback_data=f"cancel_deposit.{id}"))
        return keyboard