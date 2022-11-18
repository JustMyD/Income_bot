import os
import logging
import psycopg2 as ps

from config.configuration import DB_CONN

logs_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logs/error_logs.log'))
logging.basicConfig(filename=logs_path, format='%(asctime)s | %(levelname)s: %(message)s', level=logging.ERROR)


def new_user(user_id: str) -> bool:
    """
    Проверка на наличие пользователя в БД
    :param user_id: ID в телеграмм
    :return:
    """
    result = False
    with ps.connect(database=DB_CONN['db_name'], user=DB_CONN['db_user'],
                    password=DB_CONN['db_pass'], host=DB_CONN['db_host'], port=DB_CONN['db_port']) as db_connect:
        with db_connect.cursor() as db_cursor:
            users = []
            try:
                db_cursor.execute('''
                select telegram_id from income_bot.users
                ''')
                users = db_cursor.fetchall()
            except Exception as e:
                logging.error(f'User id {user_id}:\n{e}')
            users = (row[0] for row in users)
            result = False if user_id in users else True

    return result


def append_new_user(user_id: str, full_name: str, username: str) -> bool:
    """
    Добавление нового пользователя в БД
    :param full_name: Полное имя в телеграм
    :param username:  @username
    :param user_id:   Телеграм ID
    :return:          Результат работы
    """
    with ps.connect(database=DB_CONN['db_name'], user=DB_CONN['db_user'],
                    password=DB_CONN['db_pass'], host=DB_CONN['db_host'], port=DB_CONN['db_port']) as db_connect:
        with db_connect.cursor() as db_cursor:
            is_new_user = new_user(user_id)
            if is_new_user:
                try:
                    db_cursor.execute('''
                    insert into income_bot.users (telegram_id, full_name, user_name)
                    values (%s, %s, %s)
                    ''', (user_id, full_name, username))

                    db_cursor.execute('''
                    insert into income_bot.user_categories (user_id)
                    values (%s)
                    ''', (user_id, ))

                    result = 'Пользователь добавлен'
                except Exception as e:
                    result = 'Ошибка'
                    logging.error(f'User id {user_id}:\n{e}')
            else:
                result = 'Пользователь уже в базе'

    return result


