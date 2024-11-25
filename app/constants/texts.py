from dataclasses import dataclass


@dataclass
class Text:
    """Текстовые сообщения проекта."""

    APP_TITLE = 'QRKot'
    APP_DESCRIPTION = ('Приложение для Благотворительного фонда поддержки '
                       'котиков')

    INVALID_PASSWORD_LENGTH = 'Пароль должен содержать не менее 3 символов.'
    INVALID_PASSWORD_AS_EMAIL = ('Пароль не должен содержать адрес электронной'
                                 ' почты.')
    USER_CREATION_COMPLETED = 'Пользователь {} зарегистрирован.'

    NAME_TITLE = 'Название благотворительного проекта'
    DESCRIPTION_TITLE = 'Описание благотворительного проекта'
    FULL_AMOUNT_TITLE_PROJECT = 'Требуемая сумма'
    FULL_AMOUNT_TITLE_DONATION = 'Сумма пожертвования'
    COMMENT_TITLE = 'Комментарий к пожертвованию'

    ERROR_UNIQUE_NAME = 'Проект с таким именем уже существует!'
    ERROR_FULL_AMOUNT_UPDATE = ('Новое значение требуемой суммы не должно быть'
                                ' меньше уже внесенных средств {}')
    ERROR_NOT_FOUND = 'Нет объекта под этим id.'
    ERROR_NOT_PROJECT = 'Нет проекта под данным id.'
    ERROR_FULL_AMOUNT_GE_INVESTED_AMOUNT = (
        'Нелья установить значение full_amount меньше уже вложенной суммы.'
    )
    ERROR_FULLY_INVESTED = 'Закрытый проект нельзя редактировать!'
    ERROR_REMOVE_CHARITY_PROJECT = ('В проект были внесены средства, не '
                                    'подлежит удалению!')
    ERROR_FIELD_EMPTY = 'Поле не может быть пустым'
    ERROR_FIELD_START_OR_END_SPACE = ('Поле не может начинаться или '
                                      'заканчиваться пробелом.')

    TITLE_TABLE_GOOGLE = f'{APP_TITLE} - Отчет от '
    EXAMPLE_ID = '14hveJnbdADb5dQ3DFS78trysabwUHsqiy5Ug-n8VB5o'


@dataclass
class Tag:
    """Теги для эндпоинтов проекта."""

    AUTHENTICATION = 'Auth'
    CHARITY_PROJECT = 'Charity_project'
    DONATION = 'Donation'
    USERS = 'Users'
    GOOGLE = 'Google'


@dataclass
class TableCell:
    """Текст в ячейках Google-таблицы."""

    R1C1 = 'Отчёт от'
    R2C1 = 'Топ проектов по скорости закрытия'
    R3C1 = 'Название проекта'
    R3C2 = 'Время сбора'
    R3C3 = 'Описание'
