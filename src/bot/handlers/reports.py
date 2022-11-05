import datetime as dt

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.init_bot import bot

from bot.keyboards.inline_keyboards import make_report_type_inline_message, make_report_period_inline_message, \
    callback_data, make_year_calendar, make_month_calendar, make_day_calendar

from services.db import get_today_report, get_weekly_report, get_monthly_report, get_free_period_report

today_report_template = 'Всего {kind} за сегодня: '

weekly_report_template = 'Всего {kind} за неделю: '

monthly_report_template = 'Всего {kind} за месяц: '

free_report_template = 'Всего {kind} за выбранный период: '


async def show_report_type_message(message: types.Message):
    inline_message = make_report_type_inline_message()
    await message.answer(text='Выберите тип отчета', reply_markup=inline_message)


async def show_report_period_message(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    report_message = 'прихода' if report_type == 'income' else 'расхода'
    inline_message = make_report_period_inline_message(report_type)
    await bot.edit_message_text(text=f'Выберите период для {report_message}', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def show_today_report(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    user_id = query.from_user.id
    report = await get_today_report(user_id=str(user_id), report_type=report_type, msg_template=today_report_template)
    await query.message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_weekly_report(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    user_id = query.from_user.id
    report = await get_weekly_report(user_id=str(user_id), report_type=report_type, msg_template=weekly_report_template)
    await query.message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_monthly_report(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    user_id = query.from_user.id
    report = await get_monthly_report(user_id=str(user_id), report_type=report_type,
                                      msg_template=monthly_report_template)
    await query.message.answer(text=report, reply_markup=types.ReplyKeyboardRemove())


async def show_free_report_calendar(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    cur_date = str(dt.datetime.now().date())
    inline_message = await make_day_calendar(report_type, cur_date[:-3], current_phase='from')
    await query.message.answer(text='Выберите дату начала периода', reply_markup=inline_message)


async def change_calendar_view(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    calendar_period = callback_data.get('period', 'day')
    date_part = callback_data.get('value')
    current_phase = callback_data.get('phase')
    if calendar_period == 'year':
        inline_message = await make_year_calendar(report_type, current_phase=current_phase)
    elif calendar_period == 'month':
        inline_message = await make_month_calendar(report_type, date_part, current_phase=current_phase)
    elif calendar_period == 'day':
        inline_message = await make_day_calendar(report_type, date_part, current_phase=current_phase)
    await bot.edit_message_text(text='Выберите дату начала периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def get_free_report_start_date(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    period_from = callback_data.get('value')
    period_from = dt.datetime.strptime(period_from, '%Y-%m-%d').strftime('%Y-%m-%d')
    cur_date = str(dt.datetime.now().date())
    inline_message = await make_day_calendar(report_type, cur_date[:-3], current_phase='to')
    print(period_from)
    await query.answer(text='Дата начала периода опредлена')
    await bot.edit_message_text(text='Теперь выберите дату окончания периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def get_free_report_end_date(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    period_to = callback_data.get('value')
    period_to = dt.datetime.strptime(period_to, '%Y-%m-%d').strftime('%Y-%m-%d')
    print(period_to)
    await query.answer(text='Дата окончания период определена')


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(show_report_type_message, Text('Отчеты'))
    dp.register_callback_query_handler(show_report_period_message, callback_data['report'].filter(action='choose'))

    dp.register_callback_query_handler(show_today_report, callback_data['report'].filter(action='show', period='today'))
    dp.register_callback_query_handler(show_weekly_report, callback_data['report'].filter(action='show', period='week'))
    dp.register_callback_query_handler(show_monthly_report,
                                       callback_data['report'].filter(action='show', period='month'))

    dp.register_callback_query_handler(show_free_report_calendar, callback_data['report'].filter(action='show', period='free'))
    dp.register_callback_query_handler(change_calendar_view, callback_data['calendar'].filter(action='change'))
    dp.register_callback_query_handler(get_free_report_start_date, callback_data['calendar'].filter(action='choose', period='day', phase='from'))
    dp.register_callback_query_handler(get_free_report_end_date, callback_data['calendar'].filter(action='choose', period='day', phase='to'))
