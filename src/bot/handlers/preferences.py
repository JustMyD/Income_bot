from bot.keyboards.inline_keyboards import menu_callback_data
from bot.init_bot import bot

from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery


async def callback_show_preferences_menu(query: CallbackQuery):
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Отчеты', callback_data=menu_callback_data.new(type='reports',
                                                                                        action='show'))],
        [types.InlineKeyboardButton(text='Лимиты', callback_data=menu_callback_data.new(type='limits',
                                                                                        action='show'))],
        [types.InlineKeyboardButton(text='Категории прихода', callback_data=menu_callback_data.new(type='categories',
                                                                                                   action='income'))],
        [types.InlineKeyboardButton(text='Категории расходов', callback_data=menu_callback_data.new(type='categories',
                                                                                                    action='expense'))],
        [types.InlineKeyboardButton(text='Главное меню', callback_data=menu_callback_data.new(type='main_menu',
                                                                                              action='show'))],
    ])
    await bot.edit_message_text(text='Что хотите изменить', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


def register_preferences_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback_show_preferences_menu, menu_callback_data.filter(type='preferences',
                                                                                                 action='show'))