import random

import asyncpg

from tgbot.config import DbConfig, BinanceData

conn: asyncpg.Connection = None


async def create_conn():
    global conn
    conn = await asyncpg.connect(DbConfig.host, password=DbConfig.password)


class UsersDb:
    @staticmethod
    async def user_exists(user_id):
        query = f"select * from users where user_id = {user_id}"
        return await conn.fetchval(query)

    @staticmethod
    async def register_user(user_id):
        query = f"insert into users(user_id) values ({user_id})"
        await conn.execute(query)
        query = f"insert into user_wallets(user_id, btc_address, eth_address, usdt_address) values " \
                f"({user_id}, '{BinanceData.btc_address}', '{BinanceData.eth_address}', '{BinanceData.usdt_address}')"
        await conn.execute(query)

    @staticmethod
    async def parse_user_info(user_id):
        query = f"select * from users where user_id = {user_id}"
        return await conn.fetchval(query)

    @staticmethod
    async def parse_wallets(user_id):
        query = f"select btc_address, eth_address, usdt_address, ngn_balance from user_wallets where user_id = {user_id}"
        return await conn.fetchrow(query)

    @staticmethod
    async def parse_balance(user_id, currency=None):
        if currency:
            query = f"select {currency}_balance from user_wallets where user_id = {user_id}"
            return await conn.fetchval(query)
        else:
            query = f"select btc_balance, eth_balance, usdt_balance, ngn_balance from user_wallets where user_id = {user_id}"
            info = await conn.fetchrow(query)
            print(info)
            balances = {"BTC": info[0], "ETH": info[1], "USDT": info[2], "NGN": info[3]}
            return balances

    @staticmethod
    async def add_balance(user_id, currency, amount):
        currency = currency.lower()
        query = f"update user_wallets set {currency}_balance = {currency}_balance + {amount} where user_id = {user_id}"
        await conn.execute(query)

    @staticmethod
    async def minus_balance(user_id, currency, amount):
        query = f"update user_wallets set {currency}_balance = {currency}_balance - {amount} where user_id = {user_id}"
        await conn.execute(query)


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

    @staticmethod
    async def delete_deal(id):
        query = f"select seller_id, buyer_id from escrow where id = {id}"
        seller_id, buyer_id = await conn.fetchrow(query)
        query = f"delete from escrow where id = {id}"
        await conn.execute(query)
        return seller_id, buyer_id

    @staticmethod
    async def parse_active_deals(user_id):
        query = f"select * from escrow where seller_id = {user_id} or buyer_id = {user_id}"
        return await conn.fetch(query)

    @staticmethod
    async def accept_deal(user_id, deal_id):
        query = f"select * from escrow where id = {deal_id}"
        res = await conn.fetchrow(query)
        if user_id == res[1]:
            currency, amount, status = res[3], res[4], res[7]
            status_change = "first_status"
        else:
            currency, amount, status = res[5], res[6], res[8]
            status_change = "second_status"
        if status is True:
            return
        else:
            balance = await UsersDb.parse_balance(user_id, currency)
            if balance >= amount:
                query = f"update escrow set {status_change} = True where id = {deal_id}"
                await conn.execute(query)
                query = f"select * from escrow where id = {deal_id}"
                res = await conn.fetchrow(query)
                if res[-2] and res[-1]:
                    seller_id, first_currency, first_amount = res[0], res[2], res[3]
                    buyer_id, second_currency, second_amount = res[1], res[4], res[5]
                    if not await UsersDb.parse_balance(seller_id, first_currency) >= first_amount:
                        query = f"update escrow set 'first_status' = False where id = {deal_id}"
                        await conn.execute(query)
                        return
                    if not await UsersDb.parse_balance(buyer_id, second_currency) >= second_amount:
                        query = f"update escrow set 'second_status' = False where id = {deal_id}"
                        await conn.execute(query)
                        return
                    await UsersDb.minus_balance(seller_id, first_currency, first_amount)
                    await UsersDb.minus_balance(buyer_id, first_currency, first_amount)
                    percent = await CommissionsDb.parse_escrow_commission()
                    await UsersDb.add_balance(seller_id, second_currency, second_amount - (second_amount / 100 * percent))
                    await UsersDb.add_balance(buyer_id, first_currency, first_amount - (first_amount / 100 * percent))
                    return seller_id, buyer_id, res[0]
            else:
                return False


class CommissionsDb:
    @staticmethod
    async def parse_exchange_commission():
        query = f"select exchange_commission from service_settings"
        return await conn.fetchval(query)

    @staticmethod
    async def parse_escrow_commission():
        query = f"select escrow_exchange from service_settings"
        return await conn.fetchval(query)


class P2PDb:
    @staticmethod
    async def parse_all_orders(first_currency=None, second_currency=None):
        if first_currency:
            query = f"select * from p2p_orders where first_currency = '{second_currency}' and second_currency = '{first_currency}'"
            lst = await conn.fetch(query)
            return [i[0] for i in lst]
        else:
            query = f"select * from p2p_orders"
            lst = await conn.fetch(query)
            return [i[0] for i in lst]

    @staticmethod
    async def create_new_order(user_id, first_currency, first_amount, second_currency, second_amount):
        query = f"insert into p2p_orders(user_id, first_currency, first_amount, second_currency, second_amount) values " \
                f"({user_id}, '{first_currency}', {first_amount}, '{second_currency}', '{second_amount}')"
        await conn.execute(query)
