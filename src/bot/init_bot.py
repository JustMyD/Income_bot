"""
Основной модуль по инициалазиции бота. Здесь создается инстанс бота и диспетчера.
Основные команды:
/start - Начать диалог, авторизация пользователя, добавление его в БД, если его там нет
/help  - Подсказка по работе бота
/main  - Переход в главное меню
/feedback - Обратная связь от пользователей, шлет письмо мне на почту
/report (временная) - Отправить отчет за день
"""
import yagmail

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from bot.keyboards.reply_keyboards import make_keyboard_reply
from config.configuration import API_TOKEN, WEBHOOK_HOST
from services import user


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
callback = CallbackData('test', 'type', 'name', 'value')


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


# @dp.message_handler(Text('Настройки'))
# async def preferences(message: types.Message):
#     keyboard = make_keyboard_reply(keyboard_level='Настройки')
#     await message.answer(text='Что хотите изменить', reply_markup=keyboard)


# @dp.message_handler(Text('Главное меню'))
# async def main_menu(message: types.Message):
#     keyboard = make_keyboard_reply(keyboard_level='Главное меню')
#     await message.answer(text='Выберите действие', reply_markup=keyboard)


@dp.message_handler(commands='help')
async def show_help(message: types.Message):
    await message.answer(text=reference_msg)


class FSMTestState(StatesGroup):
    state_one = State()
    state_two = State()


@dp.message_handler(commands='test', state=None)
async def test_msg_2(message: types.Message, state: FSMContext):
    await FSMTestState.state_one.set()
    bot_message = await message.answer(text='Введите сумму')
    async with state.proxy() as data:
        data['main_msg'] = bot_message.message_id
        data['del_msg'] = []


@dp.message_handler(state=FSMTestState.state_one)
async def test_msg_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data.get('del_msg'):
            for elem in data.get('del_msg'):
                await bot.delete_message(chat_id=message.chat.id, message_id=elem)
            data['del_msg'] = []
        if message.text.isnumeric():
            inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text='Категория 1', callback_data=callback.new(type='test', name='cat_1', value=str(message.text))),
                 types.InlineKeyboardButton(text='❎', callback_data=callback.new(type='test', name='cat_1', value=str(message.text))),
                 types.InlineKeyboardButton(text='✅', callback_data='tmp'),
                 types.InlineKeyboardButton(text='Категория 2', callback_data=callback.new(type='test', name='cat_2', value=str(message.text))),
                 types.InlineKeyboardButton(text='❎', callback_data=callback.new(type='test', name='cat_2', value=str(message.text))),
                 types.InlineKeyboardButton(text='✅', callback_data='tmp')]
            ], row_width=2)
            await bot.edit_message_text(text='Выберите категорию', chat_id=message.chat.id, message_id=data['main_msg'], reply_markup=inline_message)
            data['del_msg'].append(message.message_id)
            await FSMTestState.state_two.set()
        else:
            bot_message = await message.answer(text='Сумма должна содержать только числовые значения, попробуйте еще раз')
            print(data['main_msg'])
            data['del_msg'].append(bot_message.message_id)
            data['del_msg'].append(message.message_id)


@dp.callback_query_handler(callback.filter(type='test'), state=FSMTestState.state_two)
async def test_msg_4(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        for elem in data.get('del_msg'):
            await bot.delete_message(chat_id=query.message.chat.id, message_id=elem)
        await query.answer(text='Успешно добавлена сумма', show_alert=True)
        inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Получил', callback_data='tmp'),
             types.InlineKeyboardButton(text='Потратил', callback_data='tmp')],
            [types.InlineKeyboardButton(text='Настройки', callback_data='tmp')]
        ])
        await bot.edit_message_text(text='Выберите действие', chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_message)


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
