from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.schemas.user import User
from app.db.models import User as UserModel


crypt_context = CryptContext(schemes=['sha256_crypt'])


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
        except:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')
