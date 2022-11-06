from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.init_bot import bot
from bot.keyboards.inline_keyboards import callback_data, categories_main_menu
from bot.keyboards.reply_keyboards import make_keyboard_reply
from services.db import add_new_expense, get_user_categories


class FSMExpense(StatesGroup):
    expense_sum = State()
    expense_category = State()


async def expense_state_start(message: types.Message):
    await FSMExpense.expense_sum.set()
    await message.answer(text='Отправьте сообщение с суммой расхода:', reply_markup=types.ReplyKeyboardRemove())


async def expense_state_sum(message: types.Message, state: FSMContext):
    expense_sum = message.text.strip().lower()
    if expense_sum == 'отмена':
        await state.finish()
        keyboard = make_keyboard_reply(keyboard_level='Главное меню')
        await message.answer(text='Отмена ввода', reply_markup=keyboard)
    elif expense_sum.isnumeric():
        await FSMExpense.expense_category.set()
        async with state.proxy() as data:
            remove_msg_id = data.get('remove_msg')
            if remove_msg_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=remove_msg_id)
        user_categories = get_user_categories(message.from_user.id, type='expense').split(', ')
        if user_categories:
            inline_message = categories_main_menu(user_categories, category_menu='main_menu', count=expense_sum)
            await message.answer(text='Выберите категорию:', reply_markup=inline_message)
        else:
            await message.answer(text='Не удалось получить ваши категории')
            await state.finish()
    else:
        bot_message = await message.answer(text='Ввести нужно только число, без знаков. Попробуйте еще раз')
        async with state.proxy() as data:
            remove_msg_id = data.get('remove_msg')
            if remove_msg_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=remove_msg_id)
            data['remove_msg'] = bot_message.message_id
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def expense_state_category(query: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await query.answer(cache_time=20)
    expense_sum = int(callback_data.get('value'))
    category_name = callback_data.get('name')
    result = await add_new_expense(str(query.from_user.id), expense_sum, category_name)
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')
    await query.message.answer(text=result, reply_markup=keyboard)
    await state.finish()


def register_handlers_expense(dp: Dispatcher):
    dp.register_message_handler(expense_state_start, Text('Потратил'), state=None)
    dp.register_message_handler(expense_state_sum, state=FSMExpense.expense_sum)
    dp.register_callback_query_handler(expense_state_category,
                                       callback_data['category'].filter(menu='main_menu'),
                                       state=FSMExpense.expense_category)
