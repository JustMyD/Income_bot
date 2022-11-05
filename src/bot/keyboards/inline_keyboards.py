import datetime as dt
from calendar import monthcalendar
from typing import Any, Generator, List

from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.keyboards.keyboards_mapping import MONTHS_MAPPING

callback_data = {
    'category': CallbackData('category', 'menu', 'action', 'name'),
    'report': CallbackData('report', 'type', 'action', 'period'),
    'calendar': CallbackData('calendar', 'type', 'period', 'value', 'action')
}


def categories_main_menu(categories: list, category_menu: str) -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup(row_width=1)
    for category in categories:
        inline_message.insert(types.InlineKeyboardButton(text=f'{category}',
                                                         callback_data=callback_data['category'].new(category_menu,
                                                                                                     'show', category)))
    if category_menu != 'main_menu':
        inline_message.insert(types.InlineKeyboardButton(text='Добавить категорию',
                                                         callback_data=callback_data['category'].new(category_menu,
                                                                                                     'add', 'new')))

    return inline_message


def category_edit_menu(category_name: str, category_menu: str) -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [types.InlineKeyboardButton(text='Удалить категорию',
                                    callback_data=callback_data['category'].new(category_menu, 'remove',
                                                                                category_name))],
        [types.InlineKeyboardButton(text='Назад',
                                    callback_data=callback_data['category'].new(category_menu, 'back', 'main_menu'))]
    ])
    return inline_message


def make_report_type_inline_message():
    inline_message = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [types.InlineKeyboardButton(text='Доход',
                                    callback_data=callback_data['report'].new('income', 'choose', 'empty'))],
        [types.InlineKeyboardButton(text='Расход',
                                    callback_data=callback_data['report'].new('expense', 'choose', 'empty'))]
    ])
    return inline_message


def make_report_period_inline_message(report_type: str):
    inline_message = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [types.InlineKeyboardButton(text='Отчет за сегодня', callback_data=callback_data['report'].new(type=report_type,
                                                                                                       action='show',
                                                                                                       period='today')),
         types.InlineKeyboardButton(text='Отчет за неделю', callback_data=callback_data['report'].new(type=report_type,
                                                                                                      action='show',
                                                                                                      period='week'))],
        [types.InlineKeyboardButton(text='Отчет за месяц', callback_data=callback_data['report'].new(type=report_type,
                                                                                                     action='show',
                                                                                                     period='month')),
         types.InlineKeyboardButton(text='Свой период', callback_data=callback_data['report'].new(type=report_type,
                                                                                                  action='show',
                                                                                                  period='free'))]
    ])
    return inline_message


async def make_year_calendar(report_type: str) -> types.InlineKeyboardMarkup:
    current_year = dt.datetime.now().year
    inline_keyboard = types.InlineKeyboardMarkup()
    for row in range(current_year, current_year + 12, 3):
        year_row = []
        for cell in range(row, row + 3):
            cell_callback_data = callback_data['calendar'].new(type=report_type, period='month', value=str(cell),
                                                               action='change')
            year_row.append(types.InlineKeyboardButton(text=str(cell), callback_data=cell_callback_data))
        inline_keyboard.row(*year_row)

    return inline_keyboard


async def make_month_calendar(report_type: str, date_part: str) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()
    header_callback_data = callback_data['calendar'].new(type=report_type, period='year', value='-', action='change')
    header = types.InlineKeyboardButton(text=date_part, callback_data=header_callback_data)
    inline_keyboard.row(header)
    for row in range(1, 13, 3):
        tmp_row = []
        for cell in range(row, row+3):
            cell_callback_data = callback_data['calendar'].new(type=report_type, period='day', value=f'{date_part}-{cell}', action='change')
            tmp_row.append(types.InlineKeyboardButton(text=MONTHS_MAPPING[cell], callback_data=cell_callback_data))
        inline_keyboard.row(*tmp_row)
    return inline_keyboard


async def make_day_calendar(report_type: str, date_part: str) -> types.InlineKeyboardMarkup:
    show_year = date_part.split('-')[0]
    month_number = date_part.split('-')[1]
    show_month = MONTHS_MAPPING[int(month_number)]
    month_days = monthcalendar(int(show_year), int(month_number))
    week_day_headers = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вск']
    inline_keyboard = types.InlineKeyboardMarkup()

    header = f'{show_month} {show_year}'
    header_callback_data = callback_data['calendar'].new(type=report_type, period='month', value=show_year, action='change')

    inline_keyboard.row(types.InlineKeyboardButton(text=header, callback_data=header_callback_data))
    week_day_row = [types.InlineKeyboardButton(text=name, callback_data=callback_data['calendar'].new(
        type=report_type, period='day', value=name, action='no_action'
    )) for name in week_day_headers]
    inline_keyboard.row(*week_day_row)
    for row in month_days:
        day_row = []
        for cell in row:
            button_text = str(cell) if cell else ' '
            cell_callback_data = callback_data['calendar'].new(type=report_type, period='day', value=str(cell), action='choose')
            day_row.append(types.InlineKeyboardButton(text=button_text, callback_data=cell_callback_data))
        inline_keyboard.row(*day_row)

    return inline_keyboard
