import pytest
from datetime import datetime
from app.schemas.user import User, TokenData


def test_user_schema():
    """
    Testa o schema de usuário
    """
    user = User(username='Afonso', password='pass#')

    assert user.dict() == {
        'username': 'Afonso',
        'password': 'pass#',
    }


def test_user_schema_invalid():
    """
    Testa um usuário com username inválido
    """
    with pytest.raises(ValueError):
        user = User(username='João#', password='pass#')


def test_toke_data():
    expires_at = datetime.now()

    token_data = TokenData(
        access_token='token',
        expires_at=expires_at
    )

    assert token_data.dict() == {
        'access_token': 'token',
        'expires_at': expires_at,
    }
