import os

#from aiogram.utils.executor import start_webhook
#from src.bot.init_bot import on_shutdown, on_startup

from aiogram.utils import executor

from bot.init_bot import dp
from bot.handlers import setup_dispatcher_handlers
from bot.my_filters import setup_private_filters

#WEBHOOK_PATH = ''
#WEBAPP_HOST = os.getenv('WEBAPP_HOST', default='127.0.0.1')
#WEBAPP_PORT = os.getenv('PORT', default=8003)


if __name__ == '__main__':
    setup_dispatcher_handlers(dp)
    setup_private_filters(dp)
    #start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
    executor.start_polling(dp, skip_updates=True)
