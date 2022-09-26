from functools import reduce

import psycopg2 as ps
import psycopg2.extras
from sqlalchemy import create_engine
import pandas as pd

import os
from datetime import datetime


def get_user_categories(user_id: int, type: str) -> str:
    """
    Делаем запрос к БД на получение списка категорий клиента
    :param type: Вид категорий
    :param user_id: ID в телеграмм
    :return: Список категорий
    """
    categories = ''
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost') as db_connect:
        with db_connect.cursor() as db_cursor:
            try:
                if type == 'income':
                    db_cursor.execute('''
                    select categories_income from telegram_bot.Users 
                    where telegramid = %s
                    ''', (str(user_id), ))
                elif type == 'expense':
                    db_cursor.execute('''
                    select categories_expense from telegram_bot.Users 
                    where telegramid = %s
                    ''', (str(user_id), ))
                categories = db_cursor.fetchone()[0]
            except Exception as e:
                print(e)

    return categories


async def update_user_categories(user_id: int, categories: str, type: str) -> bool:
    """
    Обновляем категории пользователя
    :param user_id: TelegramId пользователя
    :param categories: Строка с категориями
    :return:
    """
    categories_updated = False
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost') as db_connect:
        with db_connect.cursor() as db_cursor:
            try:
                if type == 'income':
                    db_cursor.execute('''
                    update telegram_bot.Users set categories_income = %s where telegramid = %s
                    ''', (categories, str(user_id)))
                elif type == 'expense':
                    db_cursor.execute('''
                    update telegram_bot.Users set categories_expense = %s where telegramid = %s
                    ''', (categories, str(user_id)))
                categories_updated = True
            except Exception as e:
                print(e)  # ToDo logger

    return categories_updated


async def add_new_income(user_id: int, income_sum: int, category: str):
    """
    Добавление в БД записи о получении средств за сегодня
    :param user_id: ID в телеграмм
    :param income_sum: Сумма прихода
    :param category: Категория
    :return: Результат работы
    """
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost',
                    cursor_factory=ps.extras.RealDictCursor) as db_connect:
        with db_connect.cursor() as db_cursor:
            result = 'Не добавлен'
            current_date_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
            today_user_incomes = None
            try:
                db_cursor.execute('''
                select * from telegram_bot.TodayIncome where user_id = %s and category = %s
                ''', (user_id, category))
                today_user_incomes = db_cursor.fetchone()
            except Exception as e:
                print(e)             # todo ДОбавить логер
                result = 'Произошла ошибка, попробуйте снова'
            if today_user_incomes:
                try:
                    db_cursor.execute('''
                    update telegram_bot.TodayIncome
                    set income_sum = income_sum + %s,
                    updated_at = %s
                    where user_id = %s and category = %s
                    ''', (income_sum, current_date_time, user_id, category))
                    result = 'Добавлен'
                except Exception as e:
                    print(e)             # todo ДОбавить логер
                    result = 'Произошла ошибка, попробуйте снова'
            else:
                try:
                    db_cursor.execute("""
                    insert into telegram_bot.TodayIncome (user_id, income_sum, category, created_at, updated_at)
                    values (%s, %s, %s, %s, %s)
                    """, (user_id, income_sum, category, current_date_time, current_date_time))
                    result = 'Добавлен'
                except Exception as e:
                    print(e)         # todo ДОбавить логер
                    result = 'Произошла ошибка, попробуйте снова'
    return result


async def add_new_expense(user_id: int, expense_sum: int, category: str):
    """
    Добавление в БД записи о расходах за сегодня
    :param user_id: ID в телеграмм
    :param expense_sum: Сумма расхода
    :param category: Категория
    :return: Результат работы
    """
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost',
                    cursor_factory=ps.extras.RealDictCursor) as db_connect:
        with db_connect.cursor() as db_cursor:
            result = 'Не добавлен'
            current_date_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
            today_user_expense = None
            try:
                db_cursor.execute('''
                select * from telegram_bot.TodayExpense where user_id = %s and category = %s
                ''', (user_id, category))
                today_user_expense = db_cursor.fetchone()
            except Exception as e:
                print(e)           # todo Добавить логер
                result = 'Произошла ошибка, попробуйте снова'
            if today_user_expense:
                try:
                    db_cursor.execute('''
                    update telegram_bot.TodayExpense
                    set expense_sum = expense_sum + %s,
                    updated_at = %s
                    where user_id = %s and category = %s
                    ''', (expense_sum, current_date_time, user_id, category))
                    result = 'Добавлен'
                except Exception as e:
                    print(e)          # todo ДОбавить логер
                    result = 'Произошла ошибка, попробуйте снова'
            else:
                try:
                    db_cursor.execute("""
                    insert into telegram_bot.TodayExpense (user_id, expense_sum, category, created_at, updated_at)
                    values (%s, %s, %s, %s, %s)
                    """, (user_id, expense_sum, category, current_date_time, current_date_time))
                    result = 'Добавлен'
                except Exception as e:
                    print(e)            # todo Добавить логер
                    result = 'Произошла ошибка, попробуйте снова'
    return result


async def get_today_reports(user_id: int) -> dict:
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost',
                    cursor_factory=ps.extras.RealDictCursor) as db_connect:
        with db_connect.cursor() as db_cursor:
            db_cursor.execute('''
            select income_sum from telegram_bot.TodayIncome where user_id = %s
            ''', (user_id, ))
            today_income = db_cursor.fetchall()
            today_income = sum(map(lambda x: x['income_sum'], today_income))
            db_cursor.execute('''
            select * from telegram_bot.TodayExpense where user_id = %s
            ''', (user_id, ))
            today_expense = db_cursor.fetchall()
            today_expense = sum(map(lambda x: x['expense_sum'], today_expense))
            data = {
                'today_income': today_income,
                'today_expense': today_expense
            }

    return data
    # db_uri = 'postgres+psycopg2://bot_user:1234@localhost/postgres'
    # engine = create_engine(db_uri, echo=True)
    # sql = (f'''
    # select * from telegram_bot.TodayIncome
    # where user_id = {user_id}
    # union all
    # select * from telegram_bot.TodayExpense
    # where user_id = {user_id}
    # ''')
    # df = pd.read_sql(sql, con=engine)
    # df = df.rename(columns={'income_sum': 'Сумма', 'category': 'Категория'})
    # df.to_html(buf='tmp.html', encoding='utf-8', index=False)


if __name__ == '__main__':
    pass
    # db_uri = 'postgres+psycopg2://bot_user:1234@localhost/postgres'
    # engine = create_engine(db_uri, echo=True)

    # conn = ps.connect(database='postgres', user='bot_user', password=1234, host='localhost')
                    # cursor_factory=ps.extras.RealDictCursor)
        # with conn.cursor() as cur:
        #     date_time_sql = 'to_char(now()::timestamp, "yyyy-mm-dd hh:mi")'

    # sql = ('''
    #                 select income_sum, category from telegram_bot.TodayIncome
    #                 ''')
    # df = pd.read_sql(sql, con=engine)
    # df = df.rename(columns={'income_sum': 'Сумма', 'category': 'Категория'})
    # df.to_html(buf='tmp.html', encoding='utf-16', index=False)
