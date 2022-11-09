import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.init_bot import bot
from bot.keyboards.inline_keyboards import menu_callback_data, transaction_callback_data
from bot.keyboards.inline_keyboards import categories_main_menu, make_main_menu_keyboard
from services.db import add_new_income, get_user_categories


class FSMGetIncome(StatesGroup):
    get_sum = State()
    get_category = State()


async def income_state_start(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await FSMGetIncome.get_sum.set()
    bot_message = await bot.edit_message_text(text='Отправьте сообщение с суммой прихода:',
                                              chat_id=query.message.chat.id,
                                              message_id=query.message.message_id)
    async with state.proxy() as data:
        data['main_msg'] = bot_message.message_id
        data['transaction_type'] = callback_data.get('type')


async def income_state_sum(message: types.Message, state: FSMContext):
    income_sum = message.text.strip().lower()
    if income_sum == 'отмена':
        inline_message = make_main_menu_keyboard()
        await message.answer(text='Выберите действие', reply_markup=inline_message)
        await state.finish()
    elif income_sum.isnumeric():
        await FSMGetIncome.get_category.set()
        async with state.proxy() as data:
            remove_msg_id = data.get('remove_msg')
            if remove_msg_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=remove_msg_id)
            data['remove_msg'] = message.message_id
            transaction_type = data.get('transaction_type')
            user_categories = get_user_categories(message.from_user.id, categories_type=transaction_type).split(', ')
            if user_categories:
                inline_message = categories_main_menu(user_categories, amount=income_sum, transaction=transaction_type)
                await bot.edit_message_text(text='Выберите категорию:', chat_id=message.chat.id,
                                            message_id=data['main_msg'], reply_markup=inline_message)
            else:
                inline_message = make_main_menu_keyboard()
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                await asyncio.sleep(2)
                await bot.edit_message_text(text='Не удалось получить ваши категории, попробуйте позднее',
                                            chat_id=message.chat.id,
                                            message_id=data['main_msg'])
                await asyncio.sleep(2)
                await bot.edit_message_text(text='Выберите действие', chat_id=message.chat.id,
                                            message_id=data['main_msg'], reply_markup=inline_message)
                await state.finish()
    else:
        bot_message = await message.answer(text='Ввести нужно только число, без знаков, попробуйте еще раз')
        async with state.proxy() as data:
            remove_msg_id = data.get('remove_msg')
            if remove_msg_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=remove_msg_id)
            data['remove_msg'] = bot_message.message_id
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def income_state_category(query: types.CallbackQuery, callback_data: dict, state=FSMContext):
    user_id = str(query.from_user.id)
    income_sum = int(callback_data.get('amount'))
    category_name = callback_data.get('category')
    result = await add_new_income(user_id, income_sum, category_name)
    async with state.proxy() as data:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=data['remove_msg'])
    if result:
        result_msg = f'Добавлено {income_sum} - {category_name}'
    else:
        result_msg = 'Произошла ошибка, попробуйте еще раз'
    await query.answer(text=result_msg, show_alert=True)
    inline_message = make_main_menu_keyboard()
    await bot.edit_message_text(text='Выберите действие', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)
    await state.finish()


def register_handlers_income(dp: Dispatcher):
    dp.register_callback_query_handler(income_state_start, menu_callback_data.filter(type='income', action='show'),
                                       state=None)
    dp.register_message_handler(income_state_sum, state=FSMGetIncome.get_sum)
    dp.register_callback_query_handler(income_state_category, transaction_callback_data.filter(type='income'),
                                       state=FSMGetIncome.get_category)
