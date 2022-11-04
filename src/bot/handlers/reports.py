import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from bot.init_bot import bot

from bot.keyboards.reply_keyboards import make_keyboard_reply
from bot.keyboards.inline_keyboards import make_report_type_inline_message, make_report_period_inline_message, callback_data
from bot.keyboards.keyboards_mapping import REPLY_KEYBOARDS_MSGS

from services.db import get_today_report, get_weekly_report, get_monthly_report

today_report_template = 'Всего {kind} за сегодня: '

weekly_report_template = 'Всего {kind} за неделю: '

monthly_report_template = 'Всего {kind} за месяц: '


async def show_report_type_message(message: types.Message):
    inline_message = make_report_type_inline_message()
    await message.answer(text='Выберите тип отчета', reply_markup=inline_message)


async def show_report_period_message(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    inline_message = make_report_period_inline_message(report_type)
    await bot.edit_message_text(text='Выберите период', message_id=query.message.message_id, reply_markup=inline_message)


async def show_today_report(message: types.Message):
    report = await get_today_report(user_id=str(message.from_user.id), report_type='expense',
                                    msg_template=today_report_template)
    await message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_weekly_report(message: types.Message):
    report = await get_weekly_report(user_id=str(message.from_user.id), report_type='expense',
                                     msg_template=weekly_report_template)
    await message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_monthly_report(message: types.Message):
    report = await get_weekly_report(user_id=str(message.from_user.id), report_type='expense',
                                     msg_template=monthly_report_template)
    await message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(show_report_type_message, Text('Отчеты'))
    dp.register_callback_query_handler(show_report_period_message, callback_data['report'].filter(action='choose'))

    dp.register_message_handler(show_today_report, Text('Отчет за сегодня'))
    dp.register_message_handler(show_weekly_report, Text('За текущую неделю'))
    dp.register_message_handler(show_monthly_report, Text('За текущий месяц'))
