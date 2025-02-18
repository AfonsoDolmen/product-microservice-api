import pytest
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import jwt
from os import getenv
from app.schemas.user import User
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases

crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')


def test_register_user(db_session):
    """
    Testa ao criar um novo usuário no banco
    """
    user = User(
        username='Afonso',
        password='pass#'
    )

    uc = UserUseCases(db_session)
    uc.register_user(user=user)

    user_on_db = db_session.query(UserModel).first()

    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)

    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_username_already_exists(db_session):
    """
    Testa se houver dois usuários com mesmo username
    """
    user_on_db = UserModel(
        username='Afonso', password=crypt_context.hash('pass#'))

    db_session.add(user_on_db)
    db_session.commit()

    uc = UserUseCases(db_session)

    user = User(username='Afonso', password=crypt_context.hash('pass#'))

    with pytest.raises(HTTPException):
        uc.register_user(user=user)

    db_session.delete(user_on_db)
    db_session.commit()


def test_user_login(db_session, user_on_db):
    """
    Testa o login do usuário e geração de Token
    """
    user = User(
        username=user_on_db.username,
        password='pass#'
    )

    uc = UserUseCases(db_session=db_session)

    token_data = uc.user_login(user=user, expires_in=30)

    assert token_data.expires_at < datetime.utcnow() + timedelta(31)


def test_user_login_invalid_username(db_session):
    """
    Testa o login do usuário com o username inválido
    """
    user = User(
        username='Invalid',
        password='pass#'
    )

    uc = UserUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.user_login(user=user, expires_in=30)


def test_user_login_invalid_password(db_session, user_on_db):
    """
    Testa o login do usuário com uma senha inválida
    """
    user = User(
        username=user_on_db.username,
        password='invalid'
    )

    uc = UserUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.user_login(user=user, expires_in=30)


def test_verify_token(db_session, user_on_db):
    """
    Teste para verificação do token
    """
    uc = UserUseCases(db_session=db_session)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    uc.verify_token(token=access_token)


def test_verify_token_expired(db_session, user_on_db):
    """
    Teste para verificação do token
    """
    uc = UserUseCases(db_session=db_session)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.utcnow() - timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException):
        uc.verify_token(token=access_token)
