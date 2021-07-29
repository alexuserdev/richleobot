from aiogram import types

from tgbot.misc.db_api.database import EscrowDb

CRYPTOS = ["BTC", "ETH", "USDT"]
WALLETS = ["BTC", "ETH", "USDT", "NGN"]


class ExchangeKeyboards:
    @staticmethod
    def main_exchange(currencys, choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for currency in currencys:
            if choose == currency:
                keyboard.insert(types.InlineKeyboardButton(text=f"✅{currency}",
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
        keyboard.insert(types.InlineKeyboardButton(text="💸Send",
                                                callback_data="send"))
        keyboard.insert(types.InlineKeyboardButton(text="💸Request",
                                                callback_data="request"))
        keyboard.insert(types.InlineKeyboardButton(text="📊Exchange",
                                                callback_data="exchange"))
        keyboard.insert(types.InlineKeyboardButton(text="Escrow exchange",
                                                   callback_data="escrow"))
        keyboard.add(types.InlineKeyboardButton(text="🎯StrikeWin lottery",
                                                callback_data="hdd"))
        return keyboard

    @staticmethod
    def deposit():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="📥Deposit",
                                                callback_data="deposit"))
        return keyboard

    @staticmethod
    def request_methods(choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if choose == wallet:
                keyboard.insert(types.InlineKeyboardButton(text=f"✅{wallet}",
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




class BalanceKeyboard:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton(text="📥Deposit",
                                                   callback_data="deposit"))
        keyboard.insert(types.InlineKeyboardButton(text="📤Withdraw",
                                                   callback_data="withdraw"))
        keyboard.insert(types.InlineKeyboardButton(text="🖨History",
                                                   callback_data="history"))
        return keyboard

    @staticmethod
    def deposit_methods(choose=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if choose == wallet:
                keyboard.insert(types.InlineKeyboardButton(text=f"✅{wallet}",
                                                           callback_data=f"deposit.{wallet}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                           callback_data=f"deposit.{wallet}"))
        return keyboard

    @staticmethod
    def deposit_check():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Check",
                                                callback_data="check"))
        return keyboard


class SettingsKeyboards:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="🌍Language",
                                                   callback_data="change_language"))
        keyboard.insert(types.InlineKeyboardButton(text="Privacy policy",
                                                   callback_data="d"))
        keyboard.insert(types.InlineKeyboardButton(text="Term of use",
                                                   callback_data="fds"))

        return keyboard

    @staticmethod
    def choose_language():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="🇬🇧English",
                                                   callback_data="language.END"))
        keyboard.insert(types.InlineKeyboardButton(text="🔙Back",
                                                   callback_data="back_settings"))
        return keyboard


class HelpKeyboards:
    @staticmethod
    def main():
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton(text="❓Ask",
                                                   callback_data="fdsf"))
        keyboard.insert(types.InlineKeyboardButton(text="🔀Exchange rates",
                                                   callback_data="exchange_rates"))
        keyboard.insert(types.InlineKeyboardButton(text="👫Community",
                                                   callback_data="oisi"))
        keyboard.insert(types.InlineKeyboardButton(text="🔢Fees",
                                                   callback_data="fees"))
        return keyboard

    @staticmethod
    def exchange_rates():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="📊Exchange",
                                                   callback_data="exchange"))
        keyboard.insert(types.InlineKeyboardButton(text="🔙Back",
                                                   callback_data="back_help"))
        return keyboard

    @staticmethod
    def fees():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="🔙Back",
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
                    keyboard.insert(types.InlineKeyboardButton(text=f"✅{wallet}",
                                                               callback_data=f"currency.{wallet}"))
                else:
                    keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                               callback_data=f"currency.{wallet}"))
        return keyboard

    @staticmethod
    async def in_deal(deal_id, status=None):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if status:
            return
        keyboard.add(types.InlineKeyboardButton(text="Accept",
                                                callback_data=f"accept_deal.{deal_id}"))
        keyboard.add(types.InlineKeyboardButton(text="Cancel deal",
                                                callback_data=f"cancel_deal.{deal_id}"))
        return keyboard
        # if status is not None:
        #     if status is False:
        #         keyboard.add(types.InlineKeyboardButton(text="Cancel",
        #                                                 callback_data="cancel_deal"))
        #         keyboard.add(types.InlineKeyboardButton(text="",
        #                                                 callback_data=))
        # else:
        #     info = await EscrowDb.parse_deal(deal_id)
        #     if user_id == info[0]:
        #         status = info[-2]
        #     elif user_id == info[1]:
        #         status = info[-1]



