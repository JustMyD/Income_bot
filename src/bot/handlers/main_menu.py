from bot.init_bot import bot
from bot.keyboards.inline_keyboards import make_main_menu_keyboard, menu_callback_data

from aiogram import types, Dispatcher


async def show_main_menu(message: types.Message):
    inline_message = make_main_menu_keyboard()
    await message.answer(text='Выберите действие', reply_markup=inline_message)


async def show_main_menu_inline(query: types.CallbackQuery):
    inline_message = make_main_menu_keyboard()
    await bot.edit_message_text(text='Выберите действие', chat_id=query.message.chat.id,
                                message_id=query.message.message_id, reply_markup=inline_message)


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(show_main_menu, commands='menu')
    dp.register_callback_query_handler(show_main_menu_inline, menu_callback_data.filter(type='main_menu'))
