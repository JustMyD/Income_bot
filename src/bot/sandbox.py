import re, json

# import pymorphy2
# import tempfile
from aiogram.utils.callback_data import CallbackData


def some_func(*args):
    string = args[0]
    regexp = re.compile(string)
    return regexp


if __name__ == '__main__':
    callback = CallbackData('category', 'action', 'name')
    another_callback = callback.new('add', 'test')

