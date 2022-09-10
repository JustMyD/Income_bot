import os

from aiogram.utils.executor import start_webhook

from src.bot.init_bot import dp, on_shutdown, on_startup, WEBHOOK_PATH
from src.bot.handlers import setup_dispatcher_handlers
from src.bot.my_filters import setup_private_filter

if __name__ == '__main__':
    WEBAPP_HOST = os.getenv('WEBAPP_HOST')
    setup_dispatcher_handlers(dp)
    setup_private_filter(dp)

    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST)
