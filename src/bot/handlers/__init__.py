from aiogram import Dispatcher

from src.bot.handlers.reports import register_handlers_report
from src.bot.handlers.limits import register_handlers_limits
from src.bot.handlers.expense_categories import register_expense_categories_handlers
from src.bot.handlers.income_categories import register_income_categories_handlers
from src.bot.handlers.expense_main import register_handlers_expense
from src.bot.handlers.income_main import register_handlers_income


def setup_dispatcher_handlers(dp: Dispatcher):
    register_handlers_report(dp)
    register_handlers_limits(dp)
    register_expense_categories_handlers(dp)
    register_income_categories_handlers(dp)
    register_handlers_income(dp)
    register_handlers_expense(dp)