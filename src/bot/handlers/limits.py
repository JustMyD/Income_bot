import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from bot.keyboards.reply_keyboards import make_keyboard_reply
from bot.keyboards.keyboards_mapping import REPLY_KEYBOARDS_MSGS


class FSMLimits(StatesGroup):
    limit_period = State()
    limit_state_period_value = State()


async def limits_state_start(message: types.Message):
    keyboard = make_keyboard_reply('Главное меню')
    await message.answer(text='В разработке', reply_markup=keyboard)
    # await FSMLimits.limit_period.set()
    # keyboard = make_keyboard_reply('Лимиты')
    # await message.answer(text='Здесь вы можете установить лимиты (необязательно)', reply_markup=keyboard)


async def limits_state_period(message: types.Message, state=FSMContext):
    if message.text == 'Главное меню':
        await state.finish()
        keyboard = make_keyboard_reply(keyboard_level=message.text)
        await message.answer(text=REPLY_KEYBOARDS_MSGS[message.text], reply_markup=keyboard)
    else:
        async with state.proxy() as data:
            data['period'] = message.text
        await FSMLimits.next()
        rm_keyboard = types.ReplyKeyboardRemove()
        await message.answer(text=REPLY_KEYBOARDS_MSGS[message.text], reply_markup=rm_keyboard)


async def limits_state_period_value(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        period = data['period']
    tmp = json.load(open('../../../test.json', 'r'))
    tmp['limits'][period] = message.text
    json.dump(tmp, open('../../../test.json', 'w'), ensure_ascii=False, indent=3)
    await state.finish()


def register_handlers_limits(dp: Dispatcher):
    dp.register_message_handler(limits_state_start, Text('Лимиты'), state=None)
    dp.register_message_handler(limits_state_period, state=FSMLimits.limit_period)
    dp.register_message_handler(limits_state_period_value, state=FSMLimits.limit_state_period_value)
