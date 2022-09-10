import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from src.bot.keyboards.reply_keyboards import make_keyboard_reply
from src.services import user

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = ''
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def greet_new_user(message: types.Message):
    user_added = user.append_new_user(message.from_user)
    if user_added:
        await message.answer(text=intro_message)
    elif not user_added:
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
    await message.answer(text='Главное меню', reply_markup=keyboard)


@dp.message_handler(commands='help')
async def show_help(message: types.Message):
    await message.answer(text=intro_message)


@dp.message_handler(commands='end')
async def hide_keyboard(message: types.Message):
    rm_keyboard = types.ReplyKeyboardRemove()
    await message.answer(text='Удачного дня!', reply_markup=rm_keyboard)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


intro_message = '''
Для того чтобы внести новый расход или 
доход за сегодня просто нажмите соответствующую 
кнопку и следуйте дальнейшим инструкциям.
В разделе настроек вы можете настроить получение 
отчетов и добавить новые категории расходов или доходов.
Для вызова справки выберите команду /help из списка команд.
'''
