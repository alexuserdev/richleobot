from concurrent.futures import ThreadPoolExecutor
from functools import partial

from aiogram import Dispatcher
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

from tgbot.config import BinanceData


client = Client(BinanceData.API_KEY, BinanceData.API_SECRET)

executor = ThreadPoolExecutor(max_workers=5)


async def get_coins_course(dp: Dispatcher):
    btc_price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol="BTCNGN"))
    eth_price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol="ETHNGN"))
    usdt_price = await dp.loop.run_in_executor(executor, partial(client.get_avg_price, symbol="USDTNGN"))
    return round(float(btc_price['price']), 2), round(float(eth_price['price']), 2), round(float(usdt_price['price']), 2)
