import pytest
from app.schemas.category import Category


def test_category_schema():
    """
    Verifica se o schema retorna um dicionário
    """
    category = Category(
        name='Roupa',
        slug='roupa'
    )

    assert category.dict() == {
        'name': 'Roupa',
        'slug': 'roupa',
    }


def test_category_schema_invalid_slug():
    """
    Verifica se o slug passado é inválido
    """
    with pytest.raises(ValueError):
        category = Category(
            name='Roupa',
            slug='roupa de cama'
        )

    with pytest.raises(ValueError):
        category = Category(
            name='Roupa',
            slug='cão'
        )

    with pytest.raises(ValueError):
        category = Category(
            name='Roupa',
            slug='Roupa'
        )
