from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from ..keyboards.inline_keboards import callback_data

from src.services.db import get_user_categories, update_user_categories
from src.bot.keyboards.inline_keboards import categories_main_menu, categories_edit_menu
from src.bot.init_bot import bot

import time

from ..keyboards.reply_keyboards import make_keyboard_reply


# async def callback_edit_category(query: types.CallbackQuery):
#     category_name = query.data.split(':')[-1]
#     message_id = query.message.message_id
#     chat_id = query.message.chat.id
#     inline_message = categories_edit_menu(category_name)
#     await bot.edit_message_text(chat_id=chat_id, text=f"Категория - {category_name}",
#                                 message_id=message_id, reply_markup=inline_message)
#
#
# async def get_back_to_categories(query: types.CallbackQuery):
#     user_categories = get_user_categories(query.from_user.id).split(', ')
#     message_id = query.message.message_id
#     chat_id = query.message.chat.id
#     if user_categories:
#         inline_message = categories_main_menu(user_categories)
#     else:
#         print("Doesn't have any category")
#     await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
#                                 message_id=message_id, reply_markup=inline_message)
#
#
# def register_handlers_categories(dp: Dispatcher):
#     dp.register_callback_query_handler(callback_edit_category, callback_data['category'].filter(menu='edit_menu', action='edit'))
#     dp.register_callback_query_handler(callback_remove_category, callback_data['category'].filter(menu='edit_menu', action='remove'))
#
#     dp.register_callback_query_handler(callback_rename_category_start,
#                                        callback_data['category'].filter(menu='edit_menu', action='rename'),
#                                        state=None)
#     dp.register_message_handler(callback_rename_category_end, state=FSMCategoryRename)
#
#     dp.register_callback_query_handler(callback_add_category_start, callback_data['category'].filter(menu='edit_menu', action='add'),
#                                        state=None)
#     dp.register_message_handler(callback_add_category_end, state=FSMCategoryAdd.category_add)
#
#     dp.register_callback_query_handler(get_back_to_categories, callback_data['category'].filter(menu='edit_menu', action='back'))
