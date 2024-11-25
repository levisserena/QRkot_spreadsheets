from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Constant, Endpoints, Text
from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Добавьте асинхронный генератор.
    Обеспечивает доступ к БД через SQLAlchemy"""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl=Endpoints.TOKEN_JWT_LOGIN)


def get_jwt_strategy() -> JWTStrategy:
    """Стратегия: хранение токена в виде JWT."""
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=Constant.LIFETIME_JWT_SECONDS
    )


auth_backend = AuthenticationBackend(
    name=Constant.NAME_AUTH_BACKEND,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Условия валидации пароля."""
        if len(password) < Constant.PASSWORD_MIN_LENGTH:
            raise InvalidPasswordException(
                reason=Text.INVALID_PASSWORD_LENGTH
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=Text.INVALID_PASSWORD_AS_EMAIL
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """Действия после успешной регистрации пользователя."""
        print(Text.USER_CREATION_COMPLETED.format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    """Корутина, возвращающая объект класса UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
