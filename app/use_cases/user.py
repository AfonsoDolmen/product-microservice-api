from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from os import getenv
from app.schemas.user import User
from app.db.models import User as UserModel
from app.schemas.user import TokenData


crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def register_user(self, user: User):
        """
        Registra um novo usuário no banco
        """
        user_model = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )

        self.db_session.add(user_model)

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')

    def user_login(self, user: User, expires_in: int = 30):
        """
        Verifica se o usuário existe no banco e gera token de acesso
        """
        user_on_db = self.db_session.query(UserModel).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

        expires_at = datetime.utcnow() + timedelta(expires_in)

        data = {
            'sub': user_on_db.username,
            'exp': expires_at
        }

        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        token_data = TokenData(access_token=access_token,
                               expires_at=expires_at)

        return token_data
