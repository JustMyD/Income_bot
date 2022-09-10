import os

from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils.executor import start_webhook
from aiohttp import web

from src.bot.init_bot import dp, on_shutdown, on_startup, WEBHOOK_URL
from src.bot.handlers import setup_dispatcher_handlers
from src.bot.my_filters import setup_private_filter

WEBAPP_HOST = os.getenv('WEBAPP_HOST')


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host=WEBAPP_HOST)

    # start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
    #               skip_updates=True, host=WEBAPP_HOST)
