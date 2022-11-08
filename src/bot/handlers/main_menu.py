from aiogram import types, Dispatcher
from bot.keyboards.inline_keyboards import make_main_menu_keyboard


async def show_main_menu(message: types.Message):
    inline_message = make_main_menu_keyboard()
    await message.answer(text='Выберите действие', reply_markup=inline_message)


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(show_main_menu, commands='menu')
