from fastapi.testclient import TestClient
from fastapi import status
from app.schemas.user import User
from app.db.models import User as UserModel
from app.main import app

client = TestClient(app)


def test_register_user_route(db_session):
    """
    Testa a rota para registrar um novo usuário
    """
    body = {
        'username': 'Afonso',
        'password': 'pass#',
    }

    response = client.post('/api/v1/user/register', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    user_on_db = db_session.query(UserModel).first()

    assert user_on_db is not None

    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_already_exists_route(user_on_db):
    """
    Testa o registro de um usuário já existente
    """
    body = {
        'username': user_on_db.username,
        'password': 'pass#',
    }

    response = client.post('/api/v1/user/register', json=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_login_route(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'pass#'
    }

    header = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/api/v1/user/login', data=body, headers=header)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'access_token' in data
    assert 'expires_at' in data


def test_user_login_route_invalid_username(user_on_db):
    body = {
        'username': 'Invalid',
        'password': 'pass#'
    }

    header = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/api/v1/user/login', data=body, headers=header)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_login_route_invalid_username(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'Invalid'
    }

    header = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/api/v1/user/login', data=body, headers=header)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
