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


class FSMExpenseCategoryAdd(StatesGroup):
    category_add = State()


class FSMExpenseCategoryRename(StatesGroup):
    category_rename = State()


async def callback_show_categories_expense(message: types.Message):
    user_categories = get_user_categories(message.from_user.id, type='expense')
    user_categories = user_categories.split(', ') if user_categories else []
    if not user_categories:
        print("Doesn't have any category")
    inline_message = categories_main_menu(user_categories, category_menu='expense_menu')
    await message.answer(text='Выберите категорию:', reply_markup=inline_message)


async def callback_edit_expense_category(query: types.CallbackQuery):
    category_name = query.data.split(':')[-1]
    message_id = query.message.message_id
    chat_id = query.message.chat.id
    inline_message = category_edit_menu(category_name, category_menu='expense_menu')
    await bot.edit_message_text(chat_id=chat_id, text=f"Категория - {category_name}",
                                message_id=message_id, reply_markup=inline_message)


async def callback_remove_expense_category(query: types.CallbackQuery):
    category_name = query.data.split(':')[-1]
    user_categories = get_user_categories(query.from_user.id, type='expense')
    user_categories = user_categories.split(', ') if user_categories else []
    message_id = query.message.message_id
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    if user_categories:
        user_categories.remove(category_name)
        user_categories_str = ', '.join(user_categories)
        await update_user_categories(user_id=user_id, categories=user_categories_str, type='expense')
        inline_message = categories_main_menu(user_categories, category_menu='expense_menu')
        await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                    message_id=message_id, reply_markup=inline_message)
    else:
        print("Doesn't have any category")


async def callback_add_expense_category_start(query: types.CallbackQuery, state: FSMContext):
    await FSMExpenseCategoryAdd.category_add.set()
    chat_id = query.message.chat.id
    keyboard = types.ReplyKeyboardRemove()
    message = await bot.send_message(chat_id=chat_id, text='Введите название категории', reply_markup=keyboard)
    async with state.proxy() as data:
        data['user_message_id'] = message.message_id
        data['inline_message_id'] = query.message.message_id


async def callback_add_expense_category_end(message: types.Message, state: FSMContext):
    category_name = message.text
    category_name = category_name.replace(',', ';')
    chat_id = message.chat.id
    if len(category_name) > 25:
        await message.answer(text='Слишком длинное название категории')
        await state.finish()
    else:
        async with state.proxy() as data:
            user_categories = get_user_categories(message.from_user.id, type='expense')
            user_categories = user_categories.split(', ') if user_categories else []
            if category_name not in user_categories:
                user_categories.append(category_name)
                inline_message = categories_main_menu(user_categories, category_menu='expense_menu')
                user_categories = ', '.join(user_categories)
                await update_user_categories(user_id=message.from_user.id, categories=user_categories, type='expense')

                await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                            message_id=data['inline_message_id'], reply_markup=inline_message)
            else:
                msg = await message.answer(text='Такая категория уже существует')
                time.sleep(2)
                await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=data['user_message_id'])
    await state.finish()


async def callback_rename_expense_category_start(query: types.CallbackQuery, state=FSMContext):
    await FSMExpenseCategoryRename.category_rename.set()
    chat_id = query.message.chat.id
    message = await bot.send_message(chat_id=chat_id, text='Новое название категории', reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as data:
        data['old_cat_name'] = query.data.split(':')[-1]
        data['user_message_id'] = message.message_id
        data['inline_message_id'] = query.message.message_id


async def callback_rename_expense_category_end(message: types.Message, state=FSMContext):
    category_name = message.text
    chat_id = message.chat.id
    if len(category_name) > 25:
        await message.answer(text='Слишком длинное название категории')
    else:
        async with state.proxy() as data:
            user_categories = get_user_categories(message.from_user.id, type='expense')
            user_categories = user_categories.replace(data['old_cat_name'], category_name)
            await update_user_categories(user_id=message.from_user.id, categories=user_categories, type='expense')
            inline_message = categories_main_menu(user_categories.split(', ') if user_categories else [],
                                                  category_menu='expense_menu')
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=data['user_message_id'])
            await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                        message_id=data['inline_message_id'], reply_markup=inline_message)
    await state.finish()


async def get_back_to_expense_categories(query: types.CallbackQuery):
    user_categories = get_user_categories(query.from_user.id, type='expense')
    user_categories = user_categories.split(', ') if user_categories else []
    message_id = query.message.message_id
    chat_id = query.message.chat.id
    if user_categories:
        inline_message = categories_main_menu(user_categories, category_menu='expense_menu')
    else:
        print("Doesn't have any category")
    await bot.edit_message_text(chat_id=chat_id, text='Выберите категорию:',
                                message_id=message_id, reply_markup=inline_message)


def register_expense_categories_handlers(dp: Dispatcher):
    dp.register_message_handler(callback_show_categories_expense, Text('Категории расходов'))
    dp.register_callback_query_handler(callback_edit_expense_category, callback_data['category'].filter(menu='expense_menu', action='show'))
    dp.register_callback_query_handler(callback_remove_expense_category, callback_data['category'].filter(menu='expense_menu', action='remove'))
    dp.register_callback_query_handler(get_back_to_expense_categories, callback_data['category'].filter(menu='expense_menu', action='back'))

    dp.register_callback_query_handler(callback_rename_expense_category_start,
                                       callback_data['category'].filter(menu='expense_menu', action='rename'),
                                       state=None)
    dp.register_message_handler(callback_rename_expense_category_end, state=FSMExpenseCategoryRename)

    dp.register_callback_query_handler(callback_add_expense_category_start, callback_data['category'].filter(menu='expense_menu', action='add'),
                                       state=None)
    dp.register_message_handler(callback_add_expense_category_end, state=FSMExpenseCategoryAdd.category_add)
