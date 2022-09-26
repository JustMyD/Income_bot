from aiogram import Dispatcher

from .filters import NotAdmin, NotPrivate, LinkFilter, IsAlNum


def setup_private_filters(dp: Dispatcher):
    dp.filters_factory.bind(NotPrivate)
    dp.filters_factory.bind(LinkFilter)
    dp.filters_factory.bind(NotAdmin)
    dp.filters_factory.bind(IsAlNum)
