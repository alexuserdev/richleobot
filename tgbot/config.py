from dataclasses import dataclass
from pathlib import Path

from envparse import env


@dataclass
class Wallets:
    btc_seed: str = 'local mushroom size account scheme camera laugh wheat parent sun wrestle supply'
    eth_seed: str = 'asset shoulder pepper token spawn chunk worth tell mixture around improve veteran'
    usdt_seed: str = 'diamond scrap return whisper entire organ loan topic pool narrow father jealous'


@dataclass
class DbConfig:
    POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
    POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
    POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="0434")
    POSTGRES_USER = env.str("POSTGRES_USER", default="postgres")
    POSTGRES_DB = env.str("POSTGRES_DB", default="aiogram")

    POSTGRES_URI = "postgresql://postgres:43154814@localhost/crypto_exchange_bot"
    #f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


@dataclass
class TgBot:
    admin_channel: int
    use_redis: bool
    token: str = env.str("TELEGRAM_TOKEN")


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
    BASE_DIR = Path(__file__).parent
    LOCALES_DIR = BASE_DIR / 'locales'
    I18N_DOMAIN = "bot"


def load_config(path: str = None):
    return Config(
        tg_bot=TgBot(
            admin_channel=-1001550460473,
            use_redis=False
        ),
    )
