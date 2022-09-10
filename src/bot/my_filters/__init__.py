from aiogram import Dispatcher

from .filters import NotAdmin, NotPrivate, LinkFilter

def setup_private_filter(dp: Dispatcher):
    dp.filters_factory.bind(NotPrivate)
    dp.filters_factory.bind(LinkFilter)
    dp.filters_factory.bind(NotAdmin)