from aiogram import types
from aiogram.utils.callback_data import CallbackData

callback_data = {
    'category': CallbackData('category', 'menu', 'action', 'name')
}


def categories_main_menu(categories: list, category_menu: str) -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup(row_width=1)
    for category in categories:
        inline_message.insert(types.InlineKeyboardButton(text=f'{category}',
                                                         callback_data=callback_data['category'].new(category_menu, 'show', category)))
    if category_menu != 'main_menu':
        inline_message.insert(types.InlineKeyboardButton(text='Добавить категорию',
                                                         callback_data=callback_data['category'].new(category_menu, 'add', 'new')))

    return inline_message


def categories_edit_menu(category_name: str, category_menu: str) -> types.InlineKeyboardMarkup:
    inline_message = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        # [types.InlineKeyboardButton(text='Изменить название',
        #                             callback_data=callback_data['category'].new(category_menu, 'rename', category_name))],
        [types.InlineKeyboardButton(text='Удалить категорию',
                                    callback_data=callback_data['category'].new(category_menu, 'remove', category_name))],
        [types.InlineKeyboardButton(text='Назад',
                                    callback_data=callback_data['category'].new(category_menu, 'back', 'main_menu'))]
    ])
    return inline_message
