from concurrent.futures import ThreadPoolExecutor
from functools import partial

from aiogram import Dispatcher
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

from tgbot.config import BinanceData
from tgbot.misc.db_api import UsersDb

client = Client(BinanceData.API_KEY, BinanceData.API_SECRET)


executor = ThreadPoolExecutor(max_workers=5)


async def course_for_coin(dp: Dispatcher, coin):
    if coin == "BTC":
        #При покупке кол-во во второй валюте
        btceth = await get_pair_price("BTC", "ETH", 1, dp)
        btcusdt = await get_pair_price("BTC", "USDT", 1, dp)
        return {"ETH": btceth, "USDT": btcusdt}
    elif coin == "ETH":
        ethbtc = await get_pair_price("ETH", "BTC", 1, dp)
        ethusdt = await get_pair_price("ETH", "USDT", 1, dp)
        return {"BTC": ethbtc, "USDT": ethusdt}
    elif coin == "USDT":
        usdtbtc = await get_pair_price("USDT", "BTC", 1, dp)
        usdteth = await get_pair_price("USDT", "ETH", 1, dp)
        return {"BTC": usdtbtc, "ETH": usdteth}


async def get_coins_course(dp: Dispatcher):
    btc_price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol="BTCNGN"))
    eth_price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol="ETHNGN"))
    usdt_price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol="USDTNGN"))
    return round(float(btc_price['price']), 2), round(float(eth_price['price']), 2), round(float(usdt_price['price']), 2)


async def get_payments(dp: Dispatcher, coin):
    payments = await dp.loop.run_in_executor(executor, partial(client.get_deposit_history, coin=coin))
    return payments


async def get_pair_price(first, second, count, dp, is_fiat=False):
    try:
        price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol=f"{first}{second}"))
        price = float(price['price'])
        return count * price
    except:
        price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol=f"{second}{first}"))
        price = float(price['price'])
        if is_fiat:
            return count * price
        return count / price


async def create_withdraw_request(user_id, currency, amount, address):
    await UsersDb.minus_balance(user_id, currency, amount)
    if currency != "NGN":
        client.withdraw(asset=currency,
                        address=address,
                        amount=amount)
