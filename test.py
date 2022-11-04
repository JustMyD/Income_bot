from datetime import datetime as dt
import datetime
from aiogram import types


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
    print(inline_keyboard)
