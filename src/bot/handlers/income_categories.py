import time

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from ..keyboards.inline_keboards import callback_data

from services.db import get_user_categories, update_user_categories
from bot.keyboards.inline_keboards import categories_main_menu, category_edit_menu
from bot.my_filters import IsAlNum
from bot.init_bot import bot


class FSMIncomeCategoryAdd(StatesGroup):
    category_add = State()


async def callback_show_categories_income(message: types.Message):
    user_categories = get_user_categories(message.from_user.id, type='income')
    user_categories = user_categories.split(', ') if user_categories else []
    if not user_categories:
        print("Doesn't have any category")
    inline_message = categories_main_menu(user_categories, category_menu='income_menu')
    await message.answer(text='Выберите категорию:', reply_markup=inline_message)


async def callback_edit_income_category(query: types.CallbackQuery):
    category_name = query.data.split(':')[-1]
    message_id = query.message.message_id
    chat_id = query.message.chat.id
    inline_message = category_edit_menu(category_name, category_menu='income_menu')
    await bot.edit_message_text(chat_id=chat_id, text=f"Категория - {category_name}",
                                message_id=message_id, reply_markup=inline_message)


async def callback_remove_income_category(query: types.CallbackQuery):
    category_name = query.data.split(':')[-1]
    user_categories = get_user_categories(query.from_user.id, type='income')
    user_categories = user_categories.split(', ') if user_categories else []
    message_id = query.message.message_id
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    if user_categories:
        user_categories.remove(category_name)
        user_categories_str = ', '.join(user_categories)
        await update_user_categories(user_id=user_id, categories=user_categories_str, type='income')
        inline_message = categories_main_menu(user_categories, category_menu='income_menu')
        await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                    message_id=message_id, reply_markup=inline_message)
    else:
        print("Doesn't have any category")


async def callback_add_income_category_start(query: types.CallbackQuery, state: FSMContext):
    await FSMIncomeCategoryAdd.category_add.set()
    chat_id = query.message.chat.id
    message = await bot.send_message(chat_id=chat_id, text='Введите название категории')
    async with state.proxy() as data:
        data['first_user_msg_id'] = message.message_id
        data['inline_message_id'] = query.message.message_id


async def callback_add_income_category_end(message: types.Message, state: FSMContext):
    category_name = message.text
    chat_id = message.chat.id
    last_user_msg = message.message_id
    if len(category_name) > 25:
        await message.answer(text='Слишком длинное название категории')
        await state.reset_state()
    else:
        async with state.proxy() as data:
            user_categories = get_user_categories(message.from_user.id, type='income')
            user_categories = user_categories.split(', ') if user_categories else []
            if category_name not in user_categories:
                user_categories.append(category_name)
                inline_message = categories_main_menu(user_categories, category_menu='income_menu')
                user_categories = ', '.join(user_categories)
                await update_user_categories(user_id=message.from_user.id, categories=user_categories, type='income')
                await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                            message_id=data['inline_message_id'], reply_markup=inline_message)
            else:
                bot_msg = await message.answer(text='Такая категория уже существует')
                time.sleep(2)
                await bot.delete_message(chat_id=chat_id, message_id=bot_msg.message_id)
            await bot.delete_message(chat_id=chat_id, message_id=last_user_msg)
            await bot.delete_message(chat_id=chat_id, message_id=data['first_user_msg_id'])
    await state.finish()


async def get_back_to_income_categories(query: types.CallbackQuery):
    user_categories = get_user_categories(query.from_user.id, type='income')
    user_categories = user_categories.split(', ') if user_categories else []
    message_id = query.message.message_id
    chat_id = query.message.chat.id
    if user_categories:
        inline_message = categories_main_menu(user_categories, category_menu='income_menu')
    else:
        print("Doesn't have any category")
    await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                message_id=message_id, reply_markup=inline_message)


def register_income_categories_handlers(dp: Dispatcher):
    dp.register_message_handler(callback_show_categories_income, Text('Категории прихода'))
    dp.register_callback_query_handler(callback_edit_income_category,
                                       callback_data['category'].filter(menu='income_menu', action='show'))
    dp.register_callback_query_handler(callback_remove_income_category,
                                       callback_data['category'].filter(menu='income_menu', action='remove'))
    dp.register_callback_query_handler(get_back_to_income_categories,
                                       callback_data['category'].filter(menu='income_menu', action='back'))

    dp.register_callback_query_handler(callback_add_income_category_start,
                                       callback_data['category'].filter(menu='income_menu', action='add'),
                                       state=None)
    dp.register_message_handler(callback_add_income_category_end, IsAlNum(), state=FSMIncomeCategoryAdd.category_add)
