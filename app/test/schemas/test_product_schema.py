import pytest
from app.schemas.product import Product, ProductInput, ProductOutput
from app.schemas.category import Category


def test_product_schema():
    """
    Testa o schema de Product
    """
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22
    )

    assert product.__dict__ == {
        'name': 'Camisa Nike',
        'slug': 'camisa-nike',
        'price': 22.99,
        'stock': 22,
    }


def test_product_schema_invalid_slug():
    """
    Testa se o slug é inválido
    """
    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Nike',
            slug='camisa nike',
            price=22.99,
            stock=22
        )

    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Nike',
            slug='cão',
            price=22.99,
            stock=22
        )

    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Nike',
            slug='Camisa-nike',
            price=22.99,
            stock=22
        )


def test_product_schema_price():
    """
    Testa o preço de Product
    """
    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Nike',
            slug='camisa-nike',
            price=0,
            stock=22
        )


def test_product_input_schema():
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22
    )

    product_input = ProductInput(
        category_slug='roupa',
        product=product
    )

    assert product_input.dict() == {
        'category_slug': 'roupa',
        'product': {
            'name': 'Camisa Nike',
            'slug': 'camisa-nike',
            'price': 22.99,
            'stock': 22,
        },
    }


def test_product_output_schema():
    category = Category(name='Roupa', slug='roupa')

    product_output = ProductOutput(
        id=1,
        name='Camisa',
        slug='camisa',
        price=10,
        stock=10,
        category=category
    )

    assert product_output.dict() == {
        'id': 1,
        'name': 'Camisa',
        'slug': 'camisa',
        'price': 10,
        'stock': 10,
        'category': {
            'name': 'Roupa',
            'slug': 'roupa',
        },
    }
