from aiogram import types

from .keyboards_mapping import REPLY_KEYBOARDS


def make_keyboard_reply(keyboard_level: str) -> object:
    keyboard = types.ReplyKeyboardMarkup()
    for btn in REPLY_KEYBOARDS[keyboard_level]:
        keyboard.row(*btn)
    return keyboard


def make_inline_message(buttons: list, pre_btn_txt: str, callback_data_txt: str) -> object:
    inline_message = types.InlineKeyboardMarkup(row_width=1)
    for btn in buttons:
        inline_message.insert(types.InlineKeyboardButton(text=f'{pre_btn_txt} - {btn}',
                                                         callback_data=f'{callback_data_txt}:{btn}'))
    return inline_message


def change_inline_message():
    pass
