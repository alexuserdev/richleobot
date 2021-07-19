import random

import asyncpg

from tgbot.config import DbConfig

conn: asyncpg.Connection = None


async def create_conn():
    global conn
    conn = await asyncpg.connect(DbConfig.host, password=DbConfig.password)


class CryptoDb:
    @staticmethod
    async def parse_index():
        query = "select count(*) from users"
        return await conn.fetchval(query) + 1


class UsersDb:
    @staticmethod
    async def user_exists(user_id):
        query = f"select * from users where user_id = {user_id}"
        return await conn.fetchval(query)

    @staticmethod
    async def register_user(user_id, wallets):
        query = f"insert into users(user_id) values ({user_id})"
        await conn.execute(query)
        query = f"insert into user_wallets(user_id, btc_address, btc_wif, eth_address, eth_wif, usdt_address, usdt_wif) values " \
                f"({user_id}, '{wallets[0][0]}', '{wallets[0][1]}', '{wallets[1][0]}', '{wallets[1][1]}', '{wallets[2][0]}', '{wallets[2][1]}')"
        await conn.execute(query)

    @staticmethod
    async def parse_user_info(user_id):
        query = f"select * from users where user_id = {user_id}"
        return await conn.fetchval(query)

    @staticmethod
    async def parse_wallets(user_id):
        query = f"select btc_address, eth_address, usdt_address, ngn_balance from user_wallets where user_id = {user_id}"
        return await conn.fetchrow(query)


class RequestsDb:
    @staticmethod
    async def create_request(user_id, currency, amount):
        if currency == "BTC":
            wallet = "btc_address"
        elif currency == "ETH":
            wallet = "eth_address"
        elif currency == "USDT":
            wallet = "usdt_address"
        else:
            return
        query = f"select {wallet} from user_wallets where user_id = {user_id}"
        wallet = await conn.fetchval(query)
        req_id = f"{user_id}{''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 5))}"
        query = f"insert into requests(id, user_id, currency, amount, wallet_number) values ({req_id}, {user_id}, " \
                f"'{currency}', {amount}, '{wallet}')"
        await conn.execute(query)
        return req_id

    @staticmethod
    async def parse_request(id):
        query = f"select * from requests where id = '{id}'"
        return await conn.fetchrow(query)

    @staticmethod
    async def delete_request(id):
        query = f"delete from requests where id = '{id}'"
        await conn.execute(query)


class EscrowDb:
    @staticmethod
    async def create_deal(info):
        query = f"insert into escrow(seller_id, buyer_id, first_currency, first_amount, second_currency, second_amount) values " \
                f"({info['seller_id']}, {info['buyer_id']}, '{info['first_currency']}', {info['first_amount']}, " \
                f"'{info['second_currency']}', {info['second_amount']}) returning id"
        return await conn.fetchval(query)

    @staticmethod
    async def parse_deal(id):
        query = f"select * from escrow where id = {id}"
        return await conn.fetchrow(query)