from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.dispatcher.filters.state import State, StatesGroup

from src.bot.keyboards.inline_keboards import callback_data, categories_main_menu
from src.bot.keyboards.reply_keyboards import make_keyboard_reply
from src.services.db import add_new_expense, get_user_categories


class FSMExpense(StatesGroup):
    expense_sum = State()
    expense_category = State()


async def expense_state_start(message: types.Message):
    await FSMExpense.expense_sum.set()
    await message.answer(text='Введите сумму расхода:', reply_markup=types.ReplyKeyboardRemove())


async def expense_state_sum(message: types.Message, state: FSMContext):
    await FSMExpense.expense_category.set()
    async with state.proxy() as data:
        data['expense_sum'] = message.text
    user_categories = get_user_categories(message.from_user.id, type='expense').split(', ')
    inline_keyboard = categories_main_menu(user_categories, category_menu='main_menu')

    await message.answer(text='Выберите категорию:', reply_markup=inline_keyboard)


async def expense_state_category(query: types.CallbackQuery, state=FSMContext):
    await query.answer(cache_time=20)
    category_name = query.data.split(':')[-1]
    async with state.proxy() as data:
        result = await add_new_expense(query.from_user.id, int(data['expense_sum']), category_name)
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')

    await query.message.answer(text=result, reply_markup=keyboard)
    await state.finish()


def register_handlers_expense(dp: Dispatcher):
    dp.register_message_handler(expense_state_start, Text('Потратил'), state=None)
    dp.register_message_handler(expense_state_sum, Regexp(r'\d+'), state=FSMExpense.expense_sum)
    dp.register_callback_query_handler(expense_state_category,
                                       callback_data['category'].filter(menu='main_menu'), state=FSMExpense.expense_category)
