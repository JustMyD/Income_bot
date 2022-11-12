"""
Основной модуль по инициалазиции бота. Здесь создается инстанс бота и диспетчера.
Основные команды:
/start - Начать диалог, авторизация пользователя, добавление его в БД, если его там нет
/help  - Подсказка по работе бота
/main  - Переход в главное меню
/feedback - Обратная связь от пользователей, шлет письмо мне на почту
/report (временная) - Отправить отчет за день
"""
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.keyboards.inline_keyboards import make_main_menu_keyboard
from config.configuration import API_TOKEN, WEBHOOK_HOST
from services import user


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def greet_new_user(message: types.Message):
    user_added = user.append_new_user(message.from_user)
    if user_added == 'Ошибка':
        greeting_message = 'Не удалось сохранить из-за ошибки, попробуйте снова позже'
    elif user_added == 'Пользователь уже в базе':
        greeting_message = 'Ваш аккаунт был добавлен ранее'
    elif user_added == 'Пользователь добавлен':
        greeting_message = f'Привет {message.from_user.full_name}'
    inline_message = make_main_menu_keyboard()
    await message.answer(text=intro_message)
    await message.answer(text=greeting_message, reply_markup=inline_message)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_HOST)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


intro_message = '''
Для того чтобы открыть список команд бота воспользуйтесь кнопкой меню, она находится слева в строке ввода текста.
Оставить отзыв можно через главное меню 
'''
