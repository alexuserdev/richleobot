from pprint import pprint

import blockcypher
from web3 import Web3
from bipwallet import wallet as wallet1
from bipwallet.utils import *
from pywallet import wallet

from tgbot.config import Wallets
from tgbot.misc.db_api.database import CryptoDb, UsersDb

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4809a65561b440e5bddcbc8e9383f029'))

def create_usdt_wallet():
    seed = wallet.generate_mnemonic()

    w = wallet.create_wallet(network='omni', seed=seed, children=1)

    return w


def create_btc_wallet():
    seed = wallet.generate_mnemonic()

    w = wallet.create_wallet(network='BTC', seed=seed, children=1)

    return w


def create_eth_wallet():
    seed = wallet.generate_mnemonic()

    w = wallet.create_wallet(network='ETH', seed=seed, children=1)

    return w


def base_wallet_create(index, network, seed):

    if network == "ETH":

        master_key = HDPrivateKey.master_key_from_mnemonic(seed)

        root_keys = HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()

        xpub = str(root_keys)

        rootkeys_wif = HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]

        xprivatekey = str(rootkeys_wif.to_b58check())

        w = wallet.create_address(network, xpub, index)

        return w['address'], xprivatekey

    else:

        master_key = HDPrivateKey.master_key_from_mnemonic(seed)

        root_keys = HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()

        xpublic_key = str(root_keys)

        address = Wallet.deserialize(xpublic_key, network=network).get_child(index, is_prime=False).to_address()

        rootkeys_wif = HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]

        xprivatekey = str(rootkeys_wif.to_b58check())

        wif = Wallet.deserialize(xprivatekey, network=network).export_to_wif()

    return address, wif


async def create_wallets(user_id):
    index = await CryptoDb.parse_index()
    wallets = []
    index = index + 1
    wallets.append(base_wallet_create(index, 'BTC', Wallets.btc_seed))
    wallets.append(base_wallet_create(index, 'ETH', Wallets.eth_seed))
    wallets.append(base_wallet_create(index, 'omni', Wallets.usdt_seed))

    await UsersDb.register_user(user_id, wallets)


async def parse_balances(user_id):
    wallets = await UsersDb.parse_wallets(user_id)
    balances = {}
    balances['BTC'] = blockcypher.get_address_details(wallets[0])['final_balance'] / 100000000
    balances['ETH'] = w3.eth.get_balance(Web3.toChecksumAddress(wallets[1])) / 100000000
    balances['USDT'] = 0
    balances['NGN'] = wallets[3]
    return balances
