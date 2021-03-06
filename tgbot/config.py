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
    admin_channel: int
    use_redis: bool


@dataclass
class BinanceData:
    # API_KEY: str = "G76QeFkMdvW9Q3MQpOHRvNP2ncs2WGHUmf7QF4NopN9jOQCafQd53CYjDKLcV6Ad"
    # API_SECRET: str = "fvbnpjKWQOIkHitbmdWv2f6u0HxP0tIjtUm0uLjjoPgmpqsKHtiwKUyU864x2MYM"
    API_KEY: str = "5Sx4RSXqlvuKClrkEunQz1kwbKPIqmf5EkCfED7QkgTT6MXva52mV6eJS4xabBXY"
    API_SECRET: str = "x1xADOmxfZyn6oyt38GWJTzl7rBmVTs3Mi1r0cGqui4ovNWg3gBeRSRDxitDOi4E"
    # btc_address: str = "19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx"
    # eth_address: str = "0xd959a62d66f50bf3646265ae6309efd6eaa18e90"
    # usdt_address: str = "0xd959a62d66f50bf3646265ae6309efd6eaa18e90"
    btc_address: str = "16ciZf1f4kcm5fjD6pzQsL84pe9uPqc644"
    eth_address: str = "0xf30f2e847cfe48b61098068f07fabaedeef6bb0d"
    usdt_address: str = "TAMKQi3VV2yffKCweqbZuXM9wepvGSnRmd"


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
            token="1944359439:AAGZ5LyAd-QXoejAPrpgxBAb-JR5QAtWpTM",
            admin_channel=-1001550460473,
            use_redis=False
        ),
        db=DbConfig(
            host="postgresql://postgres@localhost/crypto_exchange_bot",
            password="43154814",
        ),

    )
