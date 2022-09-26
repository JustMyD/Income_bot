import os

# from aiogram.utils.executor import start_webhook
# from src.bot.init_bot import dp, on_shutdown, on_startup

from aiogram.utils import executor

from src.bot.init_bot import dp
from src.bot.handlers import setup_dispatcher_handlers
from src.bot.my_filters import setup_private_filters

# WEBHOOK_PATH = ''
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = os.getenv('PORT', default=8000)


if __name__ == '__main__':
    setup_dispatcher_handlers(dp)
    setup_private_filters(dp)
    # start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
    #               skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
    executor.start_polling(dp, skip_updates=True)
