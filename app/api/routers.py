from fastapi import APIRouter

from app.api.endpoints import (charity_project_router, donation_router,
                               google_router, user_router)
from app.constants import Endpoints, Tag

main_router = APIRouter()
main_router.include_router(
    charity_project_router,
    prefix=Endpoints.CHARITY_PROJECT,
    tags=[Tag.CHARITY_PROJECT],
)
main_router.include_router(
    donation_router,
    prefix=Endpoints.DONATION,
    tags=[Tag.DONATION],
)
main_router.include_router(
    google_router,
    prefix=Endpoints.GOOGLE,
    tags=[Tag.GOOGLE],
)
main_router.include_router(user_router)
