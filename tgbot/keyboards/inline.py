from aiogram import types

from tgbot.misc.db_api.database import EscrowDb

WALLETS = ["BTC", "ETH", "USDT", "NGN"]


class ExchangeKeyboards:
    pass


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
    def choose_currency(currency=None):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for wallet in WALLETS:
            if currency == wallet:
                keyboard.insert(types.InlineKeyboardButton(text=f"✅{wallet}",
                                                           callback_data=f"currency.{wallet}"))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=wallet,
                                                           callback_data=f"currency.{wallet}"))
        return keyboard

    @staticmethod
    async def in_deal(deal_id, user_id=None, status=None):
        if status:
            pass
        else:
            info = await EscrowDb.parse_deal(deal_id)

