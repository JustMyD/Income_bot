import os

import psycopg2 as ps

from aiogram.types import base


def new_user(user_id: str) -> bool:
    """
    Проверка на наличие пользователя в БД
    :param user_id: ID в телеграмм
    :return:
    """
    result = False
    db_name = os.getenv('DATABASE_NAME')
    db_user = os.getenv('DATABASE_USER')
    db_pass = os.getenv('DATABASE_PASSWORD')
    db_host = os.getenv('DATABASE_HOST')
    db_port = os.getenv('DATABASE_PORT')
    with ps.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port) as db_connect:
        with db_connect.cursor() as db_cursor:
            users = []
            try:
                db_cursor.execute('''
                select telegramid from telegram_bot.Users
                ''')
                users = db_cursor.fetchone()
                users = users if users else ()
            except Exception as e:
                print(e)        # todo Сделать логирование
            result = False if user_id in users else True

    return result


def append_new_user(user_data: base.TelegramObject) -> bool:
    """
    Добавление нового пользователя в БД
    :param user_data: Данные о пользователе
    :return: Результат работы
    """
    db_name = os.getenv('DATABASE_NAME')
    db_user = os.getenv('DATABASE_USER')
    db_pass = os.getenv('DATABASE_PASSWORD')
    db_host = os.getenv('DATABASE_HOST')
    db_port = os.getenv('DATABASE_PORT')
    with ps.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port) as db_connect:
        with db_connect.cursor() as db_cursor:
            is_new_user = new_user(str(user_data.id))
            if is_new_user:
                try:
                    db_cursor.execute('''
                    insert into telegram_bot.Users (telegramid, fullname, username)
                    values (%s, %s, %s)
                    ''', (user_data.id, user_data.full_name, user_data.username))
                    result = True
                except Exception as e:
                    result = False
                    print(e)          # todo Сделать логирование
            else:
                result = 'Пользователь уже в базе'

    return result


