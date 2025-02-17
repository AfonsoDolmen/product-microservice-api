import pytest
from app.schemas.user import User


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
