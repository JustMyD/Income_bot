import datetime as dt

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from bot.keyboards.keyboards_mapping import MONTHS_MAPPING

callback_data = {
    'category': CallbackData('category', 'menu', 'action', 'name'),
    'report': CallbackData('report', 'type', 'action', 'period')
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


async def make_inline_calendar() -> tuple:
    current_month = MONTHS_MAPPING[dt.datetime.now().month]
    month_name = current_month[0]
    month_days = current_month[1]
    current_day = dt.datetime.now().day
    inline_message = types.InlineKeyboardMarkup(row_width=7)
    for day in list(range(1, month_days+1)):
        inline_message.add(types.InlineKeyboardButton(text=day, callback_data='tmp'))
    return inline_message, month_name
