import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.misc.db_api.database import create_conn
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.keyboard_remover import RemoveMiddleware
from tgbot.middlewares.i18n import I18nMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())
    dp.setup_middleware(RemoveMiddleware())
    dp.setup_middleware(I18nMiddleware(dp.bot["config"].I18N_DOMAIN, dp.bot["config"].LOCALES_DIR))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    from tgbot.handlers.balance import register_balance
    from tgbot.handlers.deposit import register_deposit
    from tgbot.handlers.escrow import register_escrow
    from tgbot.handlers.exchange import register_exchange
    from tgbot.handlers.operations import register_operations
    from tgbot.handlers.admin import register_admin
    from tgbot.handlers.p2p import register_p2p
    from tgbot.handlers.user import register_user
    from tgbot.handlers.start import register_start
    from tgbot.handlers.settings import register_settings
    from tgbot.handlers.help import register_help
    register_start(dp)
    register_admin(dp)
    register_operations(dp)
    register_balance(dp)
    register_deposit(dp)
    register_escrow(dp)
    register_p2p(dp)
    register_exchange(dp)
    register_settings(dp)
    register_help(dp)


async def main():
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logger.info("Starting bot")
    config = load_config()

    if config.tg_bot.use_redis:
        storage = MemoryStorage()
    else:
        storage = MemoryStorage()

    loop = asyncio.get_event_loop()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage, loop=loop)

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await create_conn()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
