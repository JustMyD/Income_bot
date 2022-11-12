import asyncio

import yagmail
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.init_bot import bot
from bot.keyboards.inline_keyboards import menu_callback_data, make_main_menu_keyboard
from config.configuration import BOT_EMAIL_USERNAME


class FSMFeedback(StatesGroup):
    feedback_start = State()


async def start_getting_feedback(query: types.CallbackQuery, state: FSMContext):
    await FSMFeedback.feedback_start.set()
    await bot.edit_message_text(text='Введите сообщение', chat_id=query.message.chat.id,
                                message_id=query.message.message_id)
    async with state.proxy() as data:
        data['main_message'] = query.message.message_id


async def send_feedback_to_owner(message: types.Message, state=FSMContext):
    to = 'commonqued@gmail.com'
    subject = 'Отзыв пользователя от бота Приход/Расход'
    body = message.text
    with yagmail.SMTP(BOT_EMAIL_USERNAME, oauth2_file='/home/www/Bot_projects/Income_bot/src/config/oauth_creds.json') as mail:
        mail.send(to=to, subject=subject, contents=body)
    bot_message = await message.answer(text='Спасибо за ваш отзыв!')
    await asyncio.sleep(1)
    inline_message = make_main_menu_keyboard()
    chat_id = message.chat.id
    async with state.proxy() as data:
        await bot.edit_message_text(text='Выберите действие:            &#x200D;', chat_id=chat_id, parse_mode='HTML',
                                    message_id=data['main_message'], reply_markup=inline_message)
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=chat_id, message_id=bot_message.message_id)
    await state.finish()


def register_handlers_feedback(dp: Dispatcher):
    dp.register_callback_query_handler(start_getting_feedback,
                                       menu_callback_data.filter(type='feedback', action='send'), state=None)
    dp.register_message_handler(send_feedback_to_owner, state=FSMFeedback.feedback_start)
