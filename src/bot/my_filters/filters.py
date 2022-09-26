import re
import typing

from aiogram import types
from aiogram.types import Message, CallbackQuery, InlineQuery, ChatMemberUpdated, ChatType
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.builtin import ChatIDArgumentType, extract_chat_ids


class NotAdmin(BoundFilter):
    def __init__(self, is_chat_admin: typing.Optional[typing.Union[ChatIDArgumentType, bool]] = None):
        self._check_current = False
        self._chat_ids = None

        if is_chat_admin is False:
            raise ValueError("is_chat_admin cannot be False")

        if not is_chat_admin:
            self._check_current = True
            return

        if isinstance(is_chat_admin, bool):
            self._check_current = is_chat_admin
        self._chat_ids = extract_chat_ids(is_chat_admin)

    @classmethod
    def validate(cls, full_config: typing.Dict[str, typing.Any]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        result = {}

        if "is_chat_admin" in full_config:
            result["is_chat_admin"] = full_config.pop("is_chat_admin")

        return result

    async def check(self, obj: typing.Union[Message, CallbackQuery, InlineQuery, ChatMemberUpdated]) -> bool:
        user_id = obj.from_user.id

        if self._check_current:
            if isinstance(obj, Message):
                chat = obj.chat
            elif isinstance(obj, CallbackQuery) and obj.message:
                chat = obj.message.chat
            elif isinstance(obj, ChatMemberUpdated):
                chat = obj.chat
            else:
                return False
            if chat.type == ChatType.PRIVATE:
                return False
            chat_ids = [chat.id]
        else:
            chat_ids = self._chat_ids

        admins = [member.user.id for chat_id in chat_ids for member in await obj.bot.get_chat_administrators(chat_id)]

        return user_id not in admins


class LinkFilter(BoundFilter):
    link_template = re.compile(r'(?:https?:\/\/)?(?:[\w\.]+)\.(?:[a-z]{2,6}\.?)(?:\/[\w\.]*)*\/?')
    exclude_links = ['umma.ru']

    async def check(self, message: types.Message):
        has_html = False
        if re.search(self.link_template, message.text):
            has_html = True
            for link in self.exclude_links:
                if link in message.text:
                    has_html = False
                    break
        return has_html


class NotPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type != types.ChatType.PRIVATE


class IsAlNum(BoundFilter):
    async def check(self, message: types.Message):
        return message.text.isalnum()


#    types.MessageEntityType.URL