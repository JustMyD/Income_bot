import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards.inline_keyboards import menu_callback_data, categories_change_menu, category_callback_data
from services.db import get_user_categories, update_user_categories, get_category_short_report
from bot.keyboards.inline_keyboards import category_edit_menu
from bot.init_bot import bot


class FSMExpenseCategoryAdd(StatesGroup):
    category_add = State()


class FSMExpenseCategoryRename(StatesGroup):
    category_rename = State()


async def callback_show_categories_change_menu(query: types.CallbackQuery, callback_data: dict):
    categories_type = callback_data.get('action')
    user_categories = get_user_categories(query.from_user.id, categories_type=categories_type)
    user_categories = user_categories.split(', ') if user_categories else []
    if not user_categories:
        print("Doesn't have any category")
    inline_message = categories_change_menu(user_categories, category_type=categories_type)
    await bot.edit_message_text(text='Выберите категорию:                        &#x200D;', chat_id=query.message.chat.id, parse_mode='HTML',
                                message_id=query.message.message_id, reply_markup=inline_message)


async def callback_edit_category(query: types.CallbackQuery, callback_data: dict):
    category_type = callback_data.get('type')
    category_name = callback_data.get('name')
    inline_message = category_edit_menu(category_name, category_type=category_type)
    out_msg = f'Категория - {category_name}\n'
    report = await get_category_short_report(user_id=str(query.from_user.id), report_type=category_type, category_name=category_name)
    out_msg += report
    await bot.edit_message_text(text=out_msg, chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def callback_remove_category(query: types.CallbackQuery, callback_data: dict):
    category_type = callback_data.get('type')
    category_name = callback_data.get('name')
    user_categories = get_user_categories(query.from_user.id, categories_type=category_type)
    user_categories = user_categories.split(', ') if user_categories else []
    if user_categories:
        user_categories.remove(category_name)
        user_categories_str = ', '.join(user_categories)
        await update_user_categories(user_id=query.from_user.id, categories=user_categories_str, categories_type=category_type)
        inline_message = categories_change_menu(user_categories, category_type=category_type)
        await bot.edit_message_text(chat_id=query.message.chat.id, text='Выберите категорию:',
                                    message_id=query.message.message_id, reply_markup=inline_message)
    else:
        print("Doesn't have any category")


async def callback_add_new_category_start(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await FSMExpenseCategoryAdd.category_add.set()
    category_type = callback_data.get('type')
    message = await bot.send_message(text='Введите название категории', chat_id=query.message.chat.id)
    async with state.proxy() as data:
        data['bot_message_id'] = message.message_id
        data['main_message_id'] = query.message.message_id
        data['remove_msg'] = []
        data['category_type'] = category_type


async def callback_add_new_category_end(message: types.Message, state: FSMContext):
    category_name = message.text
    category_name = category_name.replace(',', ';')
    async with state.proxy() as data:
        category_type = data['category_type']
        user_categories = get_user_categories(message.from_user.id, categories_type=category_type)
        user_categories = user_categories.split(', ') if user_categories else []
        if user_categories:
            if len(category_name) > 25:
                if data.get('remove_msg'):
                    for elem in data.get('remove_msg'):
                        await bot.delete_message(chat_id=message.chat.id, message_id=elem)
                bot_message = await message.answer(text='Слишком длинное название категории, введите короче')
                data['remove_msg'].append(bot_message.message_id)
            elif len(user_categories) < 10:
                if category_name not in user_categories:
                    user_categories.append(category_name)
                    inline_message = categories_change_menu(user_categories, category_type=category_type)
                    user_categories = ', '.join(user_categories)
                    await update_user_categories(user_id=message.from_user.id, categories=user_categories,
                                                 categories_type=category_type)
                    await bot.edit_message_text(text='Выберите категорию:', chat_id=message.chat.id,
                                                message_id=data['main_message_id'], reply_markup=inline_message)
                else:
                    repeat_category = await message.answer(text='Такая категория уже существует')
                    await asyncio.sleep(2)
                    await bot.delete_message(chat_id=message.chat.id, message_id=repeat_category.message_id)
            elif len(user_categories) == 10:
                await message.answer(text='Нельзя добавить больше 10 категорий')

            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=data['bot_message_id'])
            await state.finish()

        # if len(category_name) > 25:
        #     if data.get('remove_msg'):
        #         for elem in data.get('remove_msg'):
        #             await bot.delete_message(chat_id=message.chat.id, message_id=elem)
        #     bot_message = await message.answer(text='Слишком длинное название категории, введите короче')
        #     data['remove_msg'].append(bot_message.message_id)
        # elif user_categories:
        #     if len(user_categories) < 10:
        #         if category_name not in user_categories:
        #             user_categories.append(category_name)
        #             inline_message = categories_change_menu(user_categories, category_type=category_type)
        #             user_categories = ', '.join(user_categories)
        #             await update_user_categories(user_id=message.from_user.id, categories=user_categories,
        #                                          categories_type='expense')
        #             await bot.edit_message_text(text='Выберите категорию:', chat_id=message.chat.id,
        #                                         message_id=data['main_message_id'], reply_markup=inline_message)
        #         else:
        #             repeat_category = await message.answer(text='Такая категория уже существует')
        #             await asyncio.sleep(2)
        #             await bot.delete_message(chat_id=message.chat.id, message_id=repeat_category.message_id)
        #     elif len(user_categories) == 10:
        #         await message.answer(text='Нельзя добавить больше 10 категорий')
        #     await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        #     await bot.delete_message(chat_id=message.chat.id, message_id=data['bot_message_id'])
        #     await state.finish()


async def get_back_to_categories_menu(query: types.CallbackQuery, callback_data: dict):
    category_type = callback_data.get('type')
    user_categories = get_user_categories(query.from_user.id, categories_type=category_type)
    user_categories = user_categories.split(', ') if user_categories else []
    if user_categories:
        inline_message = categories_change_menu(user_categories, category_type=category_type)
    else:
        print("Doesn't have any category")
    await bot.edit_message_text(text='Выберите категорию:', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


def register_change_categories_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback_show_categories_change_menu, menu_callback_data.filter(type='categories'))
    dp.register_callback_query_handler(callback_edit_category, category_callback_data.filter(action='edit'))
    dp.register_callback_query_handler(callback_remove_category, category_callback_data.filter(action='remove'))
    dp.register_callback_query_handler(get_back_to_categories_menu, category_callback_data.filter(action='back'))

    dp.register_callback_query_handler(callback_add_new_category_start, category_callback_data.filter(action='add'),
                                       state=None)
    dp.register_message_handler(callback_add_new_category_end, state=FSMExpenseCategoryAdd.category_add)
