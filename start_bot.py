import os

from src.bot.init_bot import dp, on_shutdown, on_startup
from aiogram.utils.executor import start_webhook
from src.bot.init_bot import WEBHOOK_PATH

if __name__ == '__main__':
    WEBAPP_HOST = os.getenv('WEBAPP_HOST')

    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST)
