REPLY_KEYBOARDS = {
    'Главное меню': [
        ['Получил'],
        ['Потратил'],
        ['Настройки']
    ],
    'Отчеты': [
        ['Отчет за сегодня'],
        ['За неделю', 'За месяц', 'За квартал'],
        ['Свой период'],
        ['Главное меню']
    ],
    'Лимиты': [
        ['Дневной', 'Недельный', 'Месячный'],
        ['Квартальный'],
        ['Главное меню']
    ],
    'Настройки': [
        ['Отчеты'],
        ['Лимиты'],
        ['Категории прихода'],
        ['Категории расходов'],
        ['Главное меню']
    ]
}

REPLY_KEYBOARDS_MSGS = {
    'Главное меню': 'Выберите меню',
    'Отчеты': 'Выберите тип отчета и укажите отчетный период',
    'Лимиты': 'Здесь вы можете установить лимиты (необязательно)',
    'Дневной': 'Введите сумму лимита',
    'Недельный': 'Введите сумму лимита',
    'Месячный': 'Введите сумму лимита',
    'Квартальный': 'Введите сумму лимита',
    'За неделю': '''Примеры: "Прошлая неделя", "Позапрошлая неделя", "n неделя M месяца". Вместо n и M подставьте день и месяц.''',
    'За месяц': 'Примеры: "Август 2021 года".',
    'За квартал': 'Примеры: "1 квартал 2021 года".',
    'Свой период': 'Примеры: "30.12.2021 - 30.05.2022".',
}


if __name__ == '__main__':
    print(MAIN_MENU['Главное меню'])