from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from bot.init_bot import bot
from bot.keyboards.inline_keyboards import callback_data, categories_main_menu
from bot.keyboards.reply_keyboards import make_keyboard_reply
from services.db import add_new_income, get_user_categories


class FSMIncome(StatesGroup):
    income_sum = State()
    income_category = State()


async def income_state_start(message: types.Message):
    await FSMIncome.income_sum.set()
    await message.answer(text='Отправьте сообщение с суммой прихода:', reply_markup=types.ReplyKeyboardRemove())


async def income_state_sum(message: types.Message, state: FSMContext):
    income_sum = message.text.strip().lower()
    if income_sum == 'отмена':
        await state.finish()
        keyboard = make_keyboard_reply(keyboard_level='Главное меню')
        await message.answer(text='Отмена ввода', reply_markup=keyboard)
    elif income_sum.isnumeric():
        await FSMIncome.income_category.set()
        async with state.proxy() as data:
            remove_msg_id = data.get('remove_msg')
            if remove_msg_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=remove_msg_id)
        user_categories = get_user_categories(message.from_user.id, type='income').split(', ')
        if user_categories:
            inline_message = categories_main_menu(user_categories, category_menu='main_menu', count=income_sum)
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


async def income_state_category(query: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await query.answer(cache_time=20)
    income_sum = int(callback_data.get('value'))
    category_name = callback_data.get('name')
    result = await add_new_income(query.from_user.id, income_sum, category_name)
    keyboard = make_keyboard_reply(keyboard_level='Главное меню')
    await query.message.answer(text=result, reply_markup=keyboard)
    await state.finish()


def register_handlers_income(dp: Dispatcher):
    dp.register_message_handler(income_state_start, Text('Получил'), state=None)
    dp.register_message_handler(income_state_sum, state=FSMIncome.income_sum)
    dp.register_callback_query_handler(income_state_category,
                                       callback_data['category'].filter(menu='main_menu'),
                                       state=FSMIncome.income_category)
