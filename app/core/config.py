from typing import Optional

from pydantic import BaseSettings, EmailStr

from app.constants import Constant, Text


class Settings(BaseSettings):
    app_title: str = Text.APP_TITLE
    app_description: str = Text.APP_DESCRIPTION

    database_url: str = Constant.DATABASE_URL
    secret: str = Constant.SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    delete_user: bool = False

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = Constant.NAME_FILE_ENV


settings = Settings()
