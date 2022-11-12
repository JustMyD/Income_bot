import os

from aiogram.utils.executor import start_webhook, start_polling
from bot.init_bot import on_shutdown, on_startup

from bot.init_bot import dp
from bot.handlers import setup_dispatcher_handlers
from bot.my_filters import setup_private_filters

WEBHOOK_PATH = ''
WEBAPP_HOST = '0.0.0.0' 
WEBAPP_PORT = 8003


if __name__ == '__main__':
    setup_dispatcher_handlers(dp)
    setup_private_filters(dp)
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
    # start_polling(dp)
