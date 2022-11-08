from aiogram import Dispatcher

from bot.handlers.main_menu import register_handlers_main_menu
from bot.handlers.preferences import register_preferences_handlers
from bot.handlers.reports import register_handlers_report
from bot.handlers.limits import register_handlers_limits
from bot.handlers.get_feedback import register_handlers_feedback
from bot.handlers.change_categories import register_change_categories_handlers
from bot.handlers.get_expense import register_handlers_expense
from bot.handlers.get_income import register_handlers_income


def setup_dispatcher_handlers(dp: Dispatcher):
    register_handlers_main_menu(dp)
    register_preferences_handlers(dp)
    register_handlers_report(dp)
    register_handlers_limits(dp)
    register_handlers_feedback(dp)
    register_change_categories_handlers(dp)
    register_handlers_income(dp)
    register_handlers_expense(dp)
