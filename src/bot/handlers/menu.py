from bot.init_bot import bot
from bot.keyboards.inline_keyboards import make_main_menu_keyboard, menu_callback_data

from aiogram import types, Dispatcher

reference_msg = '''
Чтобы открыть главное меню - выберите из списка команд /menu
Добавить приход:
Главное меню -> Получил
Добавить расход:
Главное меню -> Потратил
Получить отчет за период:
Главное меню -> Настройки -> Отчеты
Изменить категории прихода:
Главное меню -> Настройки -> Категории прихода
Изменить категории расхода:
Главное меню -> Настройки -> Категории расхода
'''


async def show_main_menu(message: types.Message):
    inline_message = make_main_menu_keyboard()
    await message.answer(text='Выберите действие:            &#x200D;', reply_markup=inline_message, parse_mode='HTML')


async def show_main_menu_inline(query: types.CallbackQuery):
    inline_message = make_main_menu_keyboard()
    try:
        await bot.edit_message_text(text='Выберите действие:            &#x200D;', chat_id=query.message.chat.id, parse_mode='HTML',
                                    message_id=query.message.message_id, reply_markup=inline_message)
    except:
        await bot.send_message(text='Выберите действие:            &#x200D;', chat_id=query.message.chat.id,parse_mode='HTML',
                reply_markup=inline_message)


async def callback_show_preferences_menu(query: types.CallbackQuery):
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Отчеты', callback_data=menu_callback_data.new(type='reports',
                                                                                        action='show')),
         types.InlineKeyboardButton(text='Лимиты', callback_data=menu_callback_data.new(type='limits',
                                                                                        action='show'))],
        [types.InlineKeyboardButton(text='Категории прихода', callback_data=menu_callback_data.new(type='categories',
                                                                                                   action='income')),
         types.InlineKeyboardButton(text='Категории расходов', callback_data=menu_callback_data.new(type='categories',
                                                                                                    action='expense'))],
        [types.InlineKeyboardButton(text='Главное меню', callback_data=menu_callback_data.new(type='main_menu',
                                                                                              action='show'))],
    ])
    try:
        await bot.edit_message_text(text='Что хотите изменить:          &#x200D;', chat_id=query.message.chat.id, parse_mode='HTML',
                                    message_id=query.message.message_id, reply_markup=inline_message)
    except:
        await bot.send_message(text='Что хотите изменить:          &#x200D;', chat_id=query.message.chat.id, parse_mode='HTML',
                               reply_markup=inline_message)  


async def callback_show_help(query: types.CallbackQuery):
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Главное меню', callback_data=menu_callback_data.new(type='main_menu',
                                                                                              action='show'))]
    ])
    try:
        await bot.edit_message_text(text=reference_msg, chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    reply_markup=inline_message)
    except:
        await bot.send_message(text=reference_msg, chat_id=query.message.chat_id, reply_markup=inline_message)


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(show_main_menu, commands='menu')
    dp.register_callback_query_handler(show_main_menu_inline, menu_callback_data.filter(type='main_menu',
                                                                                        action='show'))
    dp.register_callback_query_handler(callback_show_preferences_menu, menu_callback_data.filter(type='preferences',
                                                                                                 action='show'))
    dp.register_callback_query_handler(callback_show_help, menu_callback_data.filter(type='help', action='show'))
