import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Product as ProductModel
from app.schemas.product import Product
from app.use_cases.product import ProductUseCases


def test_add_product_uc(db_session: Session, categories_on_db):
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22
    )

    uc = ProductUseCases(db_session=db_session)
    uc.add_product(product=product, category_slug=categories_on_db[0].slug)

    product_on_db = db_session.query(ProductModel).first()

    assert product_on_db is not None
    assert product_on_db.name == product.name
    assert product_on_db.slug == product.slug
    assert product_on_db.price == product.price
    assert product_on_db.stock == product.stock
    assert product_on_db.category.name == categories_on_db[0].name


def test_add_product_uc_invalid_category(db_session: Session):
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22
    )

    uc = ProductUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.add_product(product=product, category_slug='invalid')
