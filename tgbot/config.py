from dataclasses import dataclass


@dataclass
class Wallets:
    btc_seed: str = 'local mushroom size account scheme camera laugh wheat parent sun wrestle supply'
    eth_seed: str = 'asset shoulder pepper token spawn chunk worth tell mixture around improve veteran'
    usdt_seed: str = 'diamond scrap return whisper entire organ loan topic pool narrow father jealous'


@dataclass
class DbConfig:
    host: str = "postgresql://postgres@localhost/crypto_exchange_bot"
    password: str = "43154814"


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool


@dataclass
class BinanceData:
    API_KEY: str = "G76QeFkMdvW9Q3MQpOHRvNP2ncs2WGHUmf7QF4NopN9jOQCafQd53CYjDKLcV6Ad"
    API_SECRET: str = "fvbnpjKWQOIkHitbmdWv2f6u0HxP0tIjtUm0uLjjoPgmpqsKHtiwKUyU864x2MYM"


@dataclass
class CryptoInformation:
    deposit_amounts: dict

CryptoInformation = CryptoInformation(
            deposit_amounts={'BTC': [0.001, 0],
                             'ETH': [0, 0],
                             'USDT': [10, 0],
                             'NGN': [10, 5000000]})


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None):
    return Config(
        tg_bot=TgBot(
            token="1845830694:AAHDriEm2khKbhl_PDOwlAmhya6-b3FPa38",
            admin_ids=[],
            use_redis=False
        ),
        db=DbConfig(
            host="postgresql://postgres@localhost/crypto_exchange_bot",
            password="43154814",
        ),

    )
