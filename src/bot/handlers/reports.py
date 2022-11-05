from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

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
    inline_message = await make_day_calendar(report_type)
    await query.message.answer(text='Выберите дату начала периода', reply_markup=inline_message)


async def change_calendar_view(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    calendar_type = callback_data.get('period', 'day')
    if calendar_type == 'year':
        inline_message = await make_year_calendar(report_type)
    elif calendar_type == 'month':
        inline_message = await make_month_calendar(report_type)
    elif calendar_type == 'day':
        inline_message = await make_day_calendar(report_type)
    await bot.edit_message_text(text='Выберите дату начала периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def get_free_report_start_date(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    inline_message = await make_day_calendar(report_type)
    await bot.edit_message_text(text='Теперь выберите дату окончания периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def get_free_report_end_date(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    inline_message = await make_day_calendar(report_type)
    await bot.edit_message_text(text='Теперь выберите дату окончания периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


# async def show_free_report(query: types.CallbackQuery, callback_data: dict):
#     report_type = callback_data.get('type')
#     user_id = query.from_user.id
#     report = await get_free_period_report(user_id=user_id, report_type=report_type, msg_template=free_report_template,
#                                           )


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(show_report_type_message, Text('Отчеты'))
    dp.register_callback_query_handler(show_report_period_message, callback_data['report'].filter(action='choose'))

    dp.register_callback_query_handler(show_today_report, callback_data['report'].filter(action='show', period='today'))
    dp.register_callback_query_handler(show_weekly_report, callback_data['report'].filter(action='show', period='week'))
    dp.register_callback_query_handler(show_monthly_report,
                                       callback_data['report'].filter(action='show', period='month'))

    dp.register_callback_query_handler(show_free_report_calendar, callback_data['report'].filter(action='show',
                                                                                                 period='free'))
    dp.register_callback_query_handler(change_calendar_view, callback_data['calendar'].filter(action='change'))
    dp.register_callback_query_handler(get_free_report_start_date, callback_data['calendar'].filter(action='choose', period='day'))
    dp.register_callback_query_handler(get_free_report_end_date, callback_data['calendar'].filter(action='choose', period='day'))
