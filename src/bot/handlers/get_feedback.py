import yagmail
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.init_bot import bot
from bot.keyboards.inline_keyboards import menu_callback_data
from config.configuration import BOT_EMAIL_USERNAME


class FSMFeedback(StatesGroup):
    feedback_start = State()


async def start_getting_feedback(query: types.CallbackQuery):
    await FSMFeedback.feedback_start.set()
    await bot.edit_message_text(text='Введите сообщение', chat_id=query.message.chat.id,
                                message_id=query.message.message_id)


async def send_feedback_to_owner(message: types.Message, state=FSMContext):
    to = 'commonqued@gmail.com'
    subject = 'Отзыв пользователя от бота Приход/Расход'
    body = message.text
    async with yagmail.SMTP(BOT_EMAIL_USERNAME, oauth2_file='/home/www/Bot_projects/Income_bot/src/config/oauth_creds.json') as mail:
        mail.send(to=to, subject=subject, contents=body)
    await message.answer(text='Спасибо за ваш отзыв!')
    await state.finish()


def register_handlers_feedback(dp: Dispatcher):
    dp.register_callback_query_handler(start_getting_feedback,
                                       menu_callback_data.filter(type='feedback', action='send'), state=None)
    dp.register_message_handler(send_feedback_to_owner, state=FSMFeedback.feedback_start)
