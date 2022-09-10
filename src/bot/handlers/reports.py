import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from src.bot.keyboards.reply_keyboards import make_keyboard_reply
from src.bot.keyboards.keyboards_mapping import REPLY_KEYBOARDS_MSGS

from src.services.db import get_today_reports


async def get_today_report(message: types.Message):
    await get_today_reports(message.from_user.id)


class FSMReports(StatesGroup):
    report_period = State()
    report_state_period_value = State()


async def report_state_start(message: types.Message):
    await FSMReports.report_period.set()
    keyboard = make_keyboard_reply('Отчеты')
    await message.answer(text='Выберите отчетный период', reply_markup=keyboard)


async def report_state_period(message: types.Message, state=FSMContext):
    if message.text == 'Главное меню':
        await state.finish()
        keyboard = make_keyboard_reply(keyboard_level=message.text)
        await message.answer(text=REPLY_KEYBOARDS_MSGS[message.text], reply_markup=keyboard)
    else:
        async with state.proxy() as data:
            data[message.text] = ''
            data['period'] = message.text
            data['test'] = 'Тестовое сообщение'
        await FSMReports.next()
        rm_keyboard = types.ReplyKeyboardRemove()
        await message.answer(text=REPLY_KEYBOARDS_MSGS[message.text], reply_markup=rm_keyboard)


async def report_state_period_value(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        period = data['period']
    tmp = json.load(open('../../../test.json', 'r'))
    tmp['reports'][period] = message.text
    json.dump(tmp, open('../../../test.json', 'w'), ensure_ascii=False, indent=3)
    await state.finish()


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(get_today_report, Text('Отчет за сегодня'))
    dp.register_message_handler(report_state_start, Text('Отчеты'), state=None)
    dp.register_message_handler(report_state_period, state=FSMReports.report_period)
    dp.register_message_handler(report_state_period_value, state=FSMReports.report_state_period_value)
