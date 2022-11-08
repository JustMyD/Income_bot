from datetime import datetime as dt
import datetime
from aiogram import types
from calendar import monthcalendar
from bot.keyboards.keyboards_mapping import MONTHS_MAPPING


if __name__ == '__main__':
    # print(dt.now().day)
    # print(dt.now().utcnow().date() - datetime.timedelta(days=4))
    month_days = 31
    month_buttons = [
        [types.InlineKeyboardButton(text=day, callback_data='tmp') for day in list(range(week_start, week_start + 7)) if
         day <= month_days] for week_start in list(range(1, month_days + 1, 7))]
    inline_keyboard = types.InlineKeyboardMarkup(row_width=7)
    for day in list(range(1, month_days+1)):
        inline_keyboard.add(types.InlineKeyboardButton(text=day, callback_data='tmp'))
    # print(inline_keyboard)
    # print(monthcalendar(2022, 11))
    tmp = list(MONTHS_MAPPING.values())
    tmp2 = []
    for value in range(0, len(tmp), 3):
        tmp2.append(tmp[value:value+3])
    # print(tmp2)
    t = [[x*i for i in range(3)] for x in range(5)]
    t2 = [[MONTHS_MAPPING[i][0]]+[MONTHS_MAPPING[i+1][0]]+[MONTHS_MAPPING[i+2][0]] for i in range(1, 13, 3)]
