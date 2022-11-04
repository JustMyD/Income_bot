from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from bot.init_bot import bot

from bot.keyboards.inline_keyboards import make_report_type_inline_message, make_report_period_inline_message, callback_data

from services.db import get_today_report, get_weekly_report, get_monthly_report

today_report_template = 'Всего {kind} за сегодня: '

weekly_report_template = 'Всего {kind} за неделю: '

monthly_report_template = 'Всего {kind} за месяц: '


async def show_report_type_message(message: types.Message):
    inline_message = make_report_type_inline_message()
    await message.answer(text='Выберите тип отчета', reply_markup=inline_message)


async def show_report_period_message(query: types.CallbackQuery, inline_callback_data: dict):
    report_type = inline_callback_data.get('type')
    report_message = 'прихода' if report_type == 'income' else 'расхода'
    inline_message = make_report_period_inline_message(report_type)
    await bot.edit_message_text(text=f'Выберите период для {report_message}', chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_message)


async def show_today_report(query: types.CallbackQuery, inline_callback_data: dict):
    report_type = inline_callback_data.get('type')
    user_id = query.message.from_user.id
    report = await get_today_report(user_id=str(user_id), report_type=report_type, msg_template=today_report_template)
    await query.message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_weekly_report(query: types.CallbackQuery, inline_callback_data: dict):
    report_type = inline_callback_data.get('type')
    user_id = query.message.from_user.id
    report = await get_weekly_report(user_id=str(user_id), report_type=report_type, msg_template=weekly_report_template)
    await query.message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_monthly_report(query: types.CallbackQuery, inline_callback_data: dict):
    report_type = inline_callback_data.get('type')
    user_id = query.message.from_user.id
    report = await get_monthly_report(user_id=str(user_id), report_type=report_type,
                                      msg_template=monthly_report_template)
    await query.message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(show_report_type_message, Text('Отчеты'))
    dp.register_callback_query_handler(show_report_period_message, callback_data['report'].filter(action='choose'))

    dp.register_callback_query_handler(show_today_report, callback_data['report'].filter(action='show', period='today'))
    dp.register_callback_query_handler(show_weekly_report, callback_data['report'].filter(action='show', period='week'))
    dp.register_callback_query_handler(show_monthly_report, callback_data['report'].filter(action='show', period='month'))
