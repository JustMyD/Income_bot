import psycopg2 as ps

from aiogram.types import base


def new_user(user_id: str) -> bool:
    """
    Проверка на наличие пользователя в БД
    :param user_id: ID в телеграмм
    :return:
    """
    result = False
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost') as db_connect:
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
    with ps.connect(database='postgres', user='bot_user', password=1234, host='localhost') as db_connect:
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

