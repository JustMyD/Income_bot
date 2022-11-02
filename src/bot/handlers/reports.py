import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from bot.keyboards.reply_keyboards import make_keyboard_reply
from bot.keyboards.keyboards_mapping import REPLY_KEYBOARDS_MSGS

from services.db import get_today_report


class FSMReports(StatesGroup):
    report_period = State()
    report_state_period_value = State()


async def report_state_start(message: types.Message):
    keyboard = make_keyboard_reply('Отчеты')
    await message.answer(text=REPLY_KEYBOARDS_MSGS[message.text], reply_markup=keyboard)


async def show_today_report(message: types.Message):
    report = await get_today_report(user_id=str(message.from_user.id), report_type='income')
    print(report)


async def show_weekly_report(message: types.Message):
    pass


async def show_monthly_report(message: types.Message):
    pass


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(report_state_start, Text('Отчеты'))

    dp.register_message_handler(show_today_report, Text('Отчет за сегодня'))
    dp.register_message_handler(show_weekly_report, Text('За текущую неделю'))
    dp.register_message_handler(show_monthly_report, Text('За текущий месяц'))
