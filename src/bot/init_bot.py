"""
Основной модуль по инициалазиции бота. Здесь создается инстанс бота и диспетчера.
Основные команды:
/start - Начать диалог, авторизация пользователя, добавление его в БД, если его там нет
/help  - Подсказка по работе бота
/main  - Переход в главное меню
/feedback - Обратная связь от пользователей, шлет письмо мне на почту
/report (временная) - Отправить отчет за день
"""

import os
import yagmail

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from bot.keyboards.reply_keyboards import make_keyboard_reply
from config.configuration import API_TOKEN 
from services import user
from services.db import get_today_reports

#WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_HOST = 'https://tuttodorondo.ru'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def greet_new_user(message: types.Message):
    user_added = user.append_new_user(message.from_user)
    if not user_added:
        greeting_message = f'Не удалось сохранить информацию о вас, попробуйте снова'
    else:
        greeting_message = f'Привет {message.from_user.full_name}'
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')
    await message.answer(text=greeting_message, reply_markup=keyboard)


@dp.message_handler(Text('Настройки'))
async def preferences(message: types.Message):
    keyboard = make_keyboard_reply(keyboard_level='Настройки')
    await message.answer(text='Что хотите изменить', reply_markup=keyboard)


@dp.message_handler(Text('Главное меню'))
async def main_menu(message: types.Message):
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')
    await message.answer(text='Выберите действие', reply_markup=keyboard)


@dp.message_handler(commands='help')
async def show_help(message: types.Message):
    await message.answer(text=intro_message)


@dp.message_handler(commands='main')
async def show_main_menu(message: types.Message):
    keyboard = make_keyboard_reply('Главное меню')
    await message.answer(text='Выберите действие', reply_markup=keyboard)


@dp.message_handler(commands='report')
async def send_report(message: types.Message):
    report_data = await get_today_reports(message.from_user.id)
    await message.answer(text=report_message.format(income_sum=report_data['today_income'],
                                                    expense_sum=report_data['today_expense']))


@dp.message_handler(commands='feedback')
async def get_feedback(message: types.Message):
    # ToDo отправка feedback от пользователей мне на почту
    pass


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_HOST)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()
    quit()


intro_message = '''
Для того чтобы внести новый расход или 
доход за сегодня просто нажмите соответствующую 
кнопку и следуйте дальнейшим инструкциям.
В разделе настроек вы можете настроить получение 
отчетов и добавить новые категории расходов или доходов.
Для вызова справки выберите команду /help из списка команд.
'''

report_message = '''
Получено за сегодня: {income_sum}
Потрачено за сегодня: {expense_sum}
'''
