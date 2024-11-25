import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Constant:
    """Константы проекта."""

    True_ = 1
    False_ = 0

    DATABASE_URL = os.getenv('DATABASE_URL',
                             'sqlite+aiosqlite:///./fastapi.db')
    SECRET = os.getenv('SECRET', 'SECRET')
    NAME_FILE_ENV = os.getenv('NAME_FILE_ENV', '.env')

    PASSWORD_MIN_LENGTH = 3
    LIFETIME_JWT_SECONDS = int(os.getenv('LIFETIME_JWT_SECONDS', 360))
    NAME_AUTH_BACKEND = 'jwt'

    LENGTH_NAME_CHARITY_PROJECT = 100

    START_INVESTED_AMOUNT = 0
    START_INVESTED_AMOUNT_STR = str(START_INVESTED_AMOUNT)

    FULLY_INVESTED = 0
    FULLY_INVESTED_STR = str(FULLY_INVESTED)

    NAME_MIN_LENGTH = 1
    NAME_MAX_LENGTH = 100
    FULL_AMOUNT_GT = 0


SCOPES = [
    os.getenv('AUTH_SPEEEDSHEETS_URL'),
    os.getenv('DRIVE_URL'),
]


@dataclass
class ConstantGoogle:

    GET_SPEEEDSHEETS_URL: str = os.getenv('GET_SPEEEDSHEETS_URL', '')

    LOCALE = 'ru_RU'
    SHEET_TYPE = 'GRID'
    SHEET_ID = 0
    SHEET_TITLE = 'Лист1'
    ROW = 100
    COLUMN = 3
    RANGE = f'R1C1:R{ROW}C{COLUMN}'
    TYPE_PERMISSION = 'user'
    ROLE_PERMISSION = 'writer'

    FORMAT_DATETIME = '%X %x'

    MAJOR_DIMENSION = 'ROWS'
    VALUE_INPUT_OPTION = 'USER_ENTERED'


@dataclass
class Endpoints:
    """Эндпоинты проекта."""

    USERS = '/users'
    AUTHENTICATION = '/auth'
    TOKEN_JWT = '/auth/jwt'
    TOKEN_JWT_LOGIN = 'auth/jwt/login'
    CHARITY_PROJECT = '/charity_project'
    DONATION = '/donation'
    GOOGLE = '/google'
    GOOGLE_LAST = '/last'
