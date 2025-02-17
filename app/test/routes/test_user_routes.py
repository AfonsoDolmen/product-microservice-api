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
