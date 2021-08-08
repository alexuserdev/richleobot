import random

import asyncpg

from tgbot.config import DbConfig, BinanceData
from tgbot.keyboards.inline import FIAT

conn: asyncpg.Connection = None


async def create_conn():
    global conn
    conn = await asyncpg.connect(DbConfig.host, password=DbConfig.password)


class UsersDb:
    @staticmethod
    async def parse_user_id(username):
        query = f"select user_id from users where username = '{username}'"
        return await conn.fetchval(query)

    @staticmethod
    async def user_exists(user_id):
        if type(user_id) is int:
            query = f"select * from users where user_id = {user_id}"
        else:
            query = f"select * from users where username = '{user_id}'"
        return await conn.fetchval(query)

    @staticmethod
    async def update_name(user_id, full_name):
        query = f"update users set username = '{full_name}' where user_id = {user_id}"
        print(query)
        await conn.execute(query)

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
        print(query)
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
    async def create_deal(info, type):
        if type == "p2p":
            if info['second_currency'] in FIAT:
                query = f"insert into escrow(seller_id, buyer_id, first_currency, first_amount, second_currency, second_amount, second_status, type) values " \
                        f"({info['seller_id']}, {info['buyer_id']}, '{info['first_currency']}', {info['first_amount']}, " \
                        f"'{info['second_currency']}', {info['second_amount']}, True, 'p2p') returning id"

            else:
                query = f"insert into escrow(seller_id, buyer_id, first_currency, first_amount, second_currency, second_amount, first_status, type) values " \
                        f"({info['seller_id']}, {info['buyer_id']}, '{info['first_currency']}', {info['first_amount']}, " \
                        f"'{info['second_currency']}', {info['second_amount']}, True, 'p2p') returning id"
            return await conn.fetchval(query), "p2p"
        else:
            query = f"insert into escrow(seller_id, buyer_id, first_currency, first_amount, second_currency, second_amount, type) values " \
                    f"({info['seller_id']}, {info['buyer_id']}, '{info['first_currency']}', {info['first_amount']}, " \
                    f"'{info['second_currency']}', {info['second_amount']}, 'escrow') returning id"
            return await conn.fetchval(query), "escrow"

    @staticmethod
    async def parse_deal(id):
        query = f"select * from escrow where id = {id}"
        return await conn.fetchrow(query)

    @staticmethod
    async def parse_deal_chat(id):
        query = f"select link from escrow_chats where id = {id}"
        return await conn.fetchval(query)

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
                if res[-3] and res[-2]:
                    seller_id, first_currency, first_amount = res[1], res[3], res[4]
                    buyer_id, second_currency, second_amount = res[2], res[5], res[6]
                    if type == "escrow":
                        if not await UsersDb.parse_balance(seller_id, first_currency) >= first_amount:
                            query = f"update escrow set 'first_status' = False where id = {deal_id}"
                            await conn.execute(query)
                            return
                        if not await UsersDb.parse_balance(buyer_id, second_currency) >= second_amount:
                            query = f"update escrow set 'second_status' = False where id = {deal_id}"
                            await conn.execute(query)
                            return
                        query = f"delete from escrow where id = {deal_id}"
                        await conn.execute(query)
                        await UsersDb.minus_balance(seller_id, first_currency, first_amount)
                        await UsersDb.minus_balance(buyer_id, second_currency, second_amount)
                        percent = await CommissionsDb.parse_escrow_commission()
                        await UsersDb.add_balance(seller_id, second_currency, second_amount - (second_amount / 100 * percent))
                        await UsersDb.add_balance(buyer_id, first_currency, first_amount - (first_amount / 100 * percent))
                        return seller_id, buyer_id, res[0], second_currency
                    else:
                        await UsersDb.minus_balance(seller_id, first_currency, first_amount)
                        return seller_id, buyer_id, res[0], "p2p"
                else:
                    return 'Accepted'
            else:
                return False

    @staticmethod
    async def accept_fiat_deal(deal_id):
        res = await EscrowDb.parse_deal(deal_id)
        seller_id, buyer_id, currency, amount, status = res[1], res[2], res[3], res[4], res[7]
        percent = await CommissionsDb.parse_escrow_commission()
        await UsersDb.add_balance(buyer_id, currency, amount - (amount / 100 * percent))
        await conn.execute(f"delete from escrow where id = {deal_id}")
        return seller_id, buyer_id, res[0]


class CommissionsDb:
    @staticmethod
    async def parse_exchange_commission():
        query = f"select exchange_commission from service_settings"
        return await conn.fetchval(query)

    @staticmethod
    async def parse_escrow_commission():
        query = f"select escrow_exchange from service_settings"
        return await conn.fetchval(query)

    @staticmethod
    async def parse_course_percent():
        query = f"select cource_percent from service_settings"
        return await conn.fetchval(query)


class P2PDb:
    @staticmethod
    async def parse_all_orders(first_currency=None, second_currency=None, user_id=None):
        if first_currency:
            query = f"select * from p2p_orders where first_currency = '{second_currency}' and second_currency = '{first_currency}' and not user_id = '{user_id}'"
            lst = await conn.fetch(query)
            return lst
        else:
            query = f"select * from p2p_orders"
            lst = await conn.fetch(query)
            return [i[0] for i in lst]

    @staticmethod
    async def parse_users_p2p_orders(user_id):
        query = f"select * from p2p_orders where user_id = {user_id}"
        return await conn.fetch(query)

    @staticmethod
    async def delete_p2p_order(order_id):
        query = f"delete from p2p_orders where id = {order_id}"
        await conn.execute(query)

    @staticmethod
    async def create_new_order(user_id, first_currency, first_amount, second_currency, second_amount):
        query = f"insert into p2p_orders(user_id, first_currency, first_amount, second_currency, second_amount) values " \
                f"({user_id}, '{first_currency}', {first_amount}, '{second_currency}', '{second_amount}')"
        await conn.execute(query)

    @staticmethod
    async def parse_p2p_deal(deal_id):
        query = f"select * from p2p_orders where id = {deal_id}"
        return await conn.fetchrow(query)

    @staticmethod
    async def accept_p2p_order(deal_id, user_id):
        data = await P2PDb.parse_p2p_deal(deal_id)
        seller_id = data[1]
        data = {'seller_id': data[1], 'buyer_id': user_id, 'first_currency': data[2], 'first_amount': data[3],
                'second_currency': data[4], 'second_amount': data[5]}
        deal_id, status = await EscrowDb.create_deal(data, "p2p")
        return data, deal_id, status, seller_id


class AdminDb:
    @staticmethod
    async def parse_course(pair):
        query = f"select {pair} from service_settings"
        return await conn.fetchval(query)

    @staticmethod
    async def get_pair_price(first_currency, second_currency, count):
        first_currency = first_currency.lower()
        second_currency = second_currency.lower()
        first = f"{first_currency}{second_currency}"
        second = f"{second_currency}{first_currency}"
        print(first, second)
        try:
            query = f"select {first} from service_settings"
            course = await conn.fetchval(query)
            course = float(course)
            return count * course
        except:
            query = f"select {second} from service_settings"
            course = await conn.fetchval(query)
            course = float(course)
            return count / course

    @staticmethod
    async def change_param(param, value):
        if param == "course":
            param = "course_percent"
        elif param == "commission":
            param = "exchange_commission"
        else:
            raise KeyError
        query = f"update service_settings set {param} = {value}"
        await conn.execute(query)

    @staticmethod
    async def create_deposit_request(user_id, currency, amount):
        query = f"insert into deposit_request(user_id, currency, amount) values ({user_id}, '{currency}', {amount}) returning id"
        return await conn.fetchval(query)

    @staticmethod
    async def confirm_deposit_request(id):
        query = f"select * from deposit_request where id = {id}"
        id, user_id, currency, amount = await conn.fetchrow(query)
        await UsersDb.add_balance(user_id, currency, amount)
        await conn.execute(f"delete from deposit_request where id = {id}")
        return user_id


class HistoryDb:
    @staticmethod
    async def insert_into_history(user_id, type, first_currency, first_amount, second_currency=None, second_amount=None):
        query = f"insert into history(user_id, type, first_currency, first_amount, second_currency, second_amount) values " \
                f"({user_id}, '{type}', '{first_currency}', {first_amount}, '{second_currency}', {second_amount if second_amount else 0})"
        await conn.execute(query)

    @staticmethod
    async def parse_history(user_id):
        query = f"select * from history where user_id = {user_id} order by id desc limit 5"
        return await conn.fetch(query)
