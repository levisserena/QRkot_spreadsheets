from fastapi import APIRouter

from app.constants import Endpoints, Tag
from app.core.config import settings
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Роутер аутентификации пользователя.
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=Endpoints.TOKEN_JWT,
    tags=[Tag.AUTHENTICATION],
)

# Роутер регистрации пользователя.
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=Endpoints.AUTHENTICATION,
    tags=[Tag.AUTHENTICATION],
)

# Роутер управления пользователей.
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
if not settings.delete_user:
    users_router.routes = [
        rout for rout in users_router.routes if (
            rout.name != 'users:delete_user'
        )
    ]
router.include_router(
    users_router,
    prefix=Endpoints.USERS,
    tags=[Tag.USERS],
)
