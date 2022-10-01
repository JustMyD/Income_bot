from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards.inline_keboards import callback_data, categories_main_menu
from bot.keyboards.reply_keyboards import make_keyboard_reply
from services.db import add_new_income, get_user_categories


class FSMIncome(StatesGroup):
    income_sum = State()
    income_category = State()


async def income_state_start(message: types.Message):
    await FSMIncome.income_sum.set()
    await message.answer(text='Введите сумму прихода:', reply_markup=types.ReplyKeyboardRemove())


async def income_state_sum(message: types.Message, state: FSMContext):
    await FSMIncome.income_category.set()
    async with state.proxy() as data:
        data['income_sum'] = message.text
    user_categories = get_user_categories(message.from_user.id, type='income').split(', ')
    if user_categories:
        inline_message = categories_main_menu(user_categories, category_menu='main_menu')
        await message.answer(text='Выберите категорию:', reply_markup=inline_message)
    else:
        await message.answer(text='Не удалось получить ваши категории')
        await state.finish()


async def income_state_category(query: types.CallbackQuery, state=FSMContext):
    await query.answer(cache_time=20)
    category_name = query.data.split(':')[-1]
    async with state.proxy() as data:
        result = await add_new_income(query.from_user.id, int(data['income_sum']), category_name)
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')
    await query.message.answer(text=result, reply_markup=keyboard)
    await state.finish()


def register_handlers_income(dp: Dispatcher):
    dp.register_message_handler(income_state_start, Text('Получил'), state=None)
    dp.register_message_handler(income_state_sum, Regexp(r'\d+'), state=FSMIncome.income_sum)
    dp.register_callback_query_handler(income_state_category,
                                       callback_data['category'].filter(menu='main_menu'), state=FSMIncome.income_category)
