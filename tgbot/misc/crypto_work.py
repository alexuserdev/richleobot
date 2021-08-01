from datetime import datetime
from dataclasses import dataclass

from cryptoaddress import BitcoinAddress
from web3 import Web3
from dateutil.tz import tzutc

from tgbot.misc import binance_work


def check_valid(address, currency):
    if currency == "BTC":
        try:
            BitcoinAddress(address)
            return True
        except ValueError:
            return False
    elif currency == "ETH":
        if Web3.isAddress(address):
            return True
        return False
    elif currency == "NGN":
        return True


class Payment:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
        self.created: datetime = None
        self.success: bool = False

    def create(self):
        self.created = datetime.now(tz=tzutc())

    async def check(self, dp):
        payments = await binance_work.get_payments(dp, self.currency)
        for payment in payments[0:10]:
            if payment['amount'] == self.amount:
                if payment['status'] == 1:
                    return "Success"
                elif payment['status'] == 2:
                    return "Pending"
        return False

