import datetime as dt
from calendar import monthcalendar

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from bot.keyboards.keyboards_mapping import MONTHS_MAPPING

menu_callback_data = CallbackData('menu', 'type', 'action')
reports_callback_data = CallbackData('report', 'type', 'action', 'period')
category_callback_data = CallbackData('category', 'type', 'name', 'action')
transaction_callback_data = CallbackData('transaction', 'type', 'amount', 'category')
calendar_callback_data = CallbackData('calendar', 'type', 'period', 'value', 'action', 'phase', 'phase_1_value')


def make_main_menu_keyboard() -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Получил 💵➕💵',
                                    callback_data=menu_callback_data.new(type='income', action='show')),
         types.InlineKeyboardButton(text='Потратил 💸➖💸',
                                    callback_data=menu_callback_data.new(type='expense', action='show'))],
        [types.InlineKeyboardButton(text='Настройки ⚙',
                                    callback_data=menu_callback_data.new(type='preferences', action='show'))]
    ])
    return inline_message


def categories_main_menu(categories: list, amount: str, transaction: str) -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup(row_width=1)
    for category in categories:
        callback_data_button = transaction_callback_data.new(type=transaction, amount=amount, category=category)
        inline_message.insert(types.InlineKeyboardButton(text=f'{category}', callback_data=callback_data_button))
    return inline_message


def categories_change_menu(categories: list, category_type: str) -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup()
    callback_data_add_button = category_callback_data.new(type=category_type, name='new', action='add')
    callback_data_preferences_menu = menu_callback_data.new(type='preferences', action='show')
    inline_message.row(
        types.InlineKeyboardButton(text='🔙 Назад', callback_data=callback_data_preferences_menu),
        types.InlineKeyboardButton(text='🖋 Добавить категорию', callback_data=callback_data_add_button)
    )
    for category in categories:
        callback_data_button = category_callback_data.new(type=category_type, name=category, action='edit')
        inline_message.add(types.InlineKeyboardButton(text=category, callback_data=callback_data_button))
    callback_data_home_button = menu_callback_data.new(type='main_menu', action='show')
    inline_message.add(types.InlineKeyboardButton(text='🏦 Главное меню', callback_data=callback_data_home_button))
    return inline_message


def category_edit_menu(category_name: str, category_type: str) -> types.InlineKeyboardMarkup:
    callback_data_remove = category_callback_data.new(type=category_type, name=category_name, action='remove')
    callback_data_back = category_callback_data.new(type=category_type, name='empty', action='back')
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Удалить категорию', callback_data=callback_data_remove)],
        [types.InlineKeyboardButton(text='Назад', callback_data=callback_data_back)]
    ])
    return inline_message


def make_report_type_inline_message():
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Доход', callback_data=reports_callback_data.new('income', 'choose', 'empty')),
         types.InlineKeyboardButton(text='Расход',
                                    callback_data=reports_callback_data.new('expense', 'choose', 'empty'))]
    ])
    return inline_message


def make_report_period_inline_message(report_type: str):
    inline_message = types.InlineKeyboardMarkup(inline_keyboard=[
        {types.InlineKeyboardButton(text='Отчет за сегодня',
                                    callback_data=reports_callback_data.new(type=report_type, action='show',
                                                                            period='today')),
         types.InlineKeyboardButton(text='Отчет за неделю',
                                    callback_data=reports_callback_data.new(type=report_type, action='show',
                                                                            period='week'))},
        [types.InlineKeyboardButton(text='Отчет за месяц',
                                    callback_data=reports_callback_data.new(type=report_type, action='show',
                                                                            period='month')),
         types.InlineKeyboardButton(text='Свой период',
                                    callback_data=reports_callback_data.new(type=report_type, action='show',
                                                                            period='free'))]
    ])
    return inline_message


async def make_year_calendar(report_type: str, current_phase: str, phase_1_value: str) -> types.InlineKeyboardMarkup:
    current_year = dt.datetime.now().year
    inline_keyboard = types.InlineKeyboardMarkup()
    for row in range(current_year, current_year + 12, 3):
        year_row = []
        for cell in range(row, row + 3):
            cell_callback_data = calendar_callback_data.new(type=report_type, period='month', value=str(cell),
                                                            action='change', phase=current_phase,
                                                            phase_1_value=phase_1_value)
            year_row.append(types.InlineKeyboardButton(text=str(cell), callback_data=cell_callback_data))
        inline_keyboard.row(*year_row)

    return inline_keyboard


async def make_month_calendar(report_type: str, date_part: str, current_phase: str,
                              phase_1_value: str) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()
    header_callback_data = calendar_callback_data.new(type=report_type, period='year', value='-', action='change',
                                                      phase=current_phase, phase_1_value=phase_1_value)
    header = types.InlineKeyboardButton(text=date_part, callback_data=header_callback_data)
    inline_keyboard.row(header)
    for row in range(1, 13, 3):
        tmp_row = []
        for cell in range(row, row + 3):
            cell_callback_data = calendar_callback_data.new(type=report_type, period='day', value=f'{date_part}-{cell}',
                                                            action='change', phase=current_phase,
                                                            phase_1_value=phase_1_value)
            tmp_row.append(types.InlineKeyboardButton(text=MONTHS_MAPPING[cell], callback_data=cell_callback_data))
        inline_keyboard.row(*tmp_row)
    return inline_keyboard


async def make_day_calendar(report_type: str, date_part: str, current_phase: str,
                            phase_1_value: str) -> types.InlineKeyboardMarkup:
    show_year = date_part.split('-')[0]
    month_number = date_part.split('-')[1]
    show_month = MONTHS_MAPPING[int(month_number)]
    month_days = monthcalendar(int(show_year), int(month_number))
    week_day_headers = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вск']
    inline_keyboard = types.InlineKeyboardMarkup()

    header = f'{show_month} {show_year}'
    header_callback_data = calendar_callback_data.new(type=report_type, period='month', value=show_year,
                                                      action='change',
                                                      phase=current_phase, phase_1_value=phase_1_value)
    inline_keyboard.row(types.InlineKeyboardButton(text=header, callback_data=header_callback_data))
    week_day_row = [types.InlineKeyboardButton(text=name, callback_data=calendar_callback_data.new(
        type=report_type, period='day', value=name, action='no_action', phase=current_phase, phase_1_value=phase_1_value
    )) for name in week_day_headers]
    inline_keyboard.row(*week_day_row)
    for row in month_days:
        day_row = []
        for cell in row:
            if cell:
                button_text = str(cell)
                cell_callback_data_action = 'choose'
            else:
                button_text = ' '
                cell_callback_data_action = 'no_action'
            cell_callback_data = calendar_callback_data.new(type=report_type, period='day', value=f'{date_part}-{str(cell)}',
                                                            action=cell_callback_data_action, phase=current_phase,
                                                            phase_1_value=phase_1_value)
            day_row.append(types.InlineKeyboardButton(text=button_text, callback_data=cell_callback_data))
        inline_keyboard.row(*day_row)

    return inline_keyboard
