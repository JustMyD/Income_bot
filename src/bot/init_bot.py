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
from config.configuration import API_TOKEN, WEBHOOK_HOST, BOT_EMAIL_USERNAME, BOT_EMAIL_PASSWORD
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
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')
    await message.answer(text=intro_message)
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
    await message.answer(text=reference_msg)


@dp.message_handler(commands='menu')
async def show_main_menu(message: types.Message):
    keyboard = make_keyboard_reply('Главное меню')
    await message.answer(text='Выберите действие', reply_markup=keyboard)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_HOST)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()
    quit()


intro_message = '''
Для того чтобы открыть список команд бота воспользуйтесь кнопкой меню, она находится слева в строке ввода текста.
Если вы столкнулись с трудностью - выберите /help чтобы посмотреть справку
Если хотите оставить пожелание или дать обратную связь - выберите /feedback чтобы оставить анонимный отзыв 
'''

reference_msg = '''
Чтобы открыть главное меню - выберите из списка команд /main
Добавить приход:
Главное меню -> Приход
Добавить расход:
Главное меню -> Расход
Получить отчет за период:
Главное меню -> Настройки -> Отчеты
Добавить или удалить категории для прихода:
Главное меню -> Настройки -> Категории прихода
Добавить или удалить категории для расхода:
Главное меню -> Настройки -> Категории расхода
'''
