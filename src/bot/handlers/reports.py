import asyncio
import datetime as dt

from aiogram import types, Dispatcher

from bot.init_bot import bot
from bot.keyboards.inline_keyboards import menu_callback_data, reports_callback_data, calendar_callback_data
from bot.keyboards.inline_keyboards import make_report_type_inline_message, make_report_period_inline_message, \
    make_main_menu_keyboard
from bot.keyboards.inline_keyboards import make_year_calendar, make_month_calendar, make_day_calendar

from services.db import get_today_report, get_weekly_report, get_monthly_report, get_free_period_report

today_report_template = 'Всего {kind} за сегодня: {average_sum}\n'

weekly_report_template = 'Всего {kind} за неделю: {average_sum}\n'

monthly_report_template = 'Всего {kind} за месяц: {average_sum}\n'

free_report_template = '''
Период {start} - {end}

Всего {kind} {average_sum}
'''


async def show_report_type_message(query: types.CallbackQuery):
    inline_message = make_report_type_inline_message()
    await bot.edit_message_text(text='Выберите тип отчета                     &#x200D;', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message, parse_mode='HTML')


async def show_report_period_message(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    report_message = 'прихода' if report_type == 'income' else 'расхода'
    inline_message = make_report_period_inline_message(report_type)
    await bot.edit_message_text(text=f'Выберите период для {report_message}', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message, parse_mode='HTML')


async def show_today_report(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    user_id = query.from_user.id
    report = await get_today_report(user_id=str(user_id), report_type=report_type, msg_template=today_report_template)
    if report:
        callback_data_home_button = menu_callback_data.new(type='main_menu', action='show')
        inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Главное меню', callback_data=callback_data_home_button)]
        ])
        await bot.edit_message_text(text=report, chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    reply_markup=inline_message, parse_mode='HTML')
    else:
        await query.answer(text='Произошла ошибка, попробуйте еще раз', show_alert=True)
        inline_message = make_main_menu_keyboard()
        await bot.edit_message_text(text='Выберите действие:                      &#x200D;', chat_id=query.message.chat.id,
                                    message_id=query.message.message_id, reply_markup=inline_message, parse_mode='HTML')


async def show_weekly_report(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    user_id = query.from_user.id
    report = await get_weekly_report(user_id=str(user_id), report_type=report_type, msg_template=weekly_report_template)
    if report:
        callback_data_home_button = menu_callback_data.new(type='main_menu', action='show')
        inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Главное меню', callback_data=callback_data_home_button)]
        ])
        await bot.edit_message_text(text=report, chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    reply_markup=inline_message, parse_mode='HTML')
    else:
        await query.answer(text='Произошла ошибка, попробуйте еще раз', show_alert=True)
        inline_message = make_main_menu_keyboard()
        await bot.edit_message_text(text='Выберите действие:                      &#x200D;', chat_id=query.message.chat.id,
                                    message_id=query.message.message_id, reply_markup=inline_message, parse_mode='HTML')


async def show_monthly_report(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    user_id = query.from_user.id
    report = await get_monthly_report(user_id=str(user_id), report_type=report_type,
                                      msg_template=monthly_report_template)
    if report:
        callback_data_home_button = menu_callback_data.new(type='main_menu', action='show')
        inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Главное меню', callback_data=callback_data_home_button)]
        ])
        await bot.edit_message_text(text=report, chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    reply_markup=inline_message, parse_mode='HTML')
    else:
        await query.answer(text='Произошла ошибка, попробуйте еще раз', show_alert=True)
        inline_message = make_main_menu_keyboard()
        await bot.edit_message_text(text='Выберите действие:                      &#x200D;', chat_id=query.message.chat.id,
                                    message_id=query.message.message_id, reply_markup=inline_message, parse_mode='HTML')


async def show_free_report_calendar(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    cur_date = str(dt.datetime.now().date())
    inline_message = await make_day_calendar(report_type, cur_date[:-3], current_phase='from', phase_1_value='')
    await bot.edit_message_text(text='Выберите дату начала периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def change_calendar_view(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    calendar_period = callback_data.get('period', 'day')
    date_part = callback_data.get('value')
    current_phase = callback_data.get('phase')
    phase_1_value = callback_data.get('phase_1_value')
    if calendar_period == 'year':
        inline_message = await make_year_calendar(report_type, current_phase=current_phase, phase_1_value=phase_1_value)
    elif calendar_period == 'month':
        inline_message = await make_month_calendar(report_type, date_part, current_phase=current_phase,
                                                   phase_1_value=phase_1_value)
    elif calendar_period == 'day':
        inline_message = await make_day_calendar(report_type, date_part, current_phase=current_phase,
                                                 phase_1_value=phase_1_value)
    await bot.edit_message_text(text='Выберите дату начала периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def get_free_report_start_date(query: types.CallbackQuery, callback_data: dict):
    report_type = callback_data.get('type')
    period_from = callback_data.get('value')
    period_from = dt.datetime.strptime(period_from, '%Y-%m-%d').strftime('%Y-%m-%d')
    cur_date = str(dt.datetime.now().date())
    inline_message = await make_day_calendar(report_type, cur_date[:-3], current_phase='to', phase_1_value=period_from)
    await query.answer(text='Дата начала периода опредлена')
    await bot.edit_message_text(text='Теперь выберите дату окончания периода', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


async def get_free_report_end_date(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    report_type = callback_data.get('type')
    period_from = callback_data.get('phase_1_value')
    period_to = callback_data.get('value')
    period_to = dt.datetime.strptime(period_to, '%Y-%m-%d').strftime('%Y-%m-%d')
    report = await get_free_period_report(user_id=str(user_id), report_type=report_type,
                                          msg_template=free_report_template, period_start=period_from,
                                          period_end=period_to)
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Главное меню', callback_data=menu_callback_data.new(type='main_menu',
                                                                                              action='show'))]
    ])
    # inline_message = make_main_menu_keyboard()
    await bot.edit_message_text(text=report, chat_id=query.message.chat.id, parse_mode='HTML',
                                message_id=query.message.message_id, reply_markup=inline_message)
    # bot_message = await query.message.answer(text='Ожидайте')
    # await asyncio.sleep(2)
    # await bot.edit_message_text(text=report, chat_id=query.message.chat.id, message_id=bot_message.message_id)


async def handle_empty_calendar_button(query: types.CallbackQuery):
    """
    Заглушка для пустых кнопок, чтобы эти запросы не тормозили обработку запросов в CallbackQuery
    """
    pass


def register_handlers_report(dp: Dispatcher):
    dp.register_callback_query_handler(show_report_type_message, menu_callback_data.filter(type='reports',
                                                                                           action='show'))
    dp.register_callback_query_handler(show_report_period_message, reports_callback_data.filter(action='choose'))

    dp.register_callback_query_handler(show_today_report, reports_callback_data.filter(action='show', period='today'))
    dp.register_callback_query_handler(show_weekly_report, reports_callback_data.filter(action='show', period='week'))
    dp.register_callback_query_handler(show_monthly_report, reports_callback_data.filter(action='show', period='month'))

    dp.register_callback_query_handler(show_free_report_calendar, reports_callback_data.filter(action='show',
                                                                                               period='free'))
    dp.register_callback_query_handler(change_calendar_view, calendar_callback_data.filter(action='change'))
    dp.register_callback_query_handler(get_free_report_start_date,
                                       calendar_callback_data.filter(action='choose', period='day', phase='from'))
    dp.register_callback_query_handler(get_free_report_end_date,
                                       calendar_callback_data.filter(action='choose', period='day', phase='to'))

    dp.register_callback_query_handler(handle_empty_calendar_button, calendar_callback_data.filter(period='day',
                                                                                                   action='no_action'))
