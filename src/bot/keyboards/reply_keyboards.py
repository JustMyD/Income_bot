from aiogram import types

from .keyboards_mapping import REPLY_KEYBOARDS


def make_keyboard_reply(keyboard_level: str) -> object:
    keyboard = types.ReplyKeyboardMarkup()
    for btn in REPLY_KEYBOARDS[keyboard_level]:
        keyboard.row(*btn)
    return keyboard