from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from os import getenv
from app.db.connection import Session as DBSession
from app.use_cases.user import UserUseCases

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

TEST_MODE = bool(int(getenv('TEST_MODE')))


def get_db_session():
    """
    Cria e retorna uma nova sessão no banco
    """
    try:
        session = DBSession()
        yield session
    finally:
        session.close()


def auth(
    db_session: Session = Depends(get_db_session),
    token: OAuth2PasswordBearer = Depends(oauth_scheme)
):
    if TEST_MODE:
        return

    uc = UserUseCases(db_session=db_session)
    uc.verify_token(token=token)
