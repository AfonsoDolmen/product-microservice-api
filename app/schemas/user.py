import re
from pydantic import validator
from datetime import datetime
from app.schemas.base import CustomBaseModel


class User(CustomBaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        """
        Valida o username
        """
        if not re.match('^([a-z]|[A-Z]|[0-9]|-|_|@)+$', value):
            raise ValueError('Invalid username')

        return value


class TokenData(CustomBaseModel):
    access_token: str
    expires_at: datetime
