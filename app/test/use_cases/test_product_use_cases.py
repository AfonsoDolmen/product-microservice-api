import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi_pagination import Page
from app.db.models import Product as ProductModel
from app.schemas.product import Product, ProductOutput
from app.use_cases.product import ProductUseCases


def test_add_product_uc(db_session, categories_on_db):
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22,
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
        stock=22,
    )

    uc = ProductUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.add_product(product=product, category_slug='invalid')


def test_update_product(db_session: Session, product_on_db):
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22
    )

    uc = ProductUseCases(db_session=db_session)
    uc.update_product(id=product_on_db.id, product=product)

    product_updated_on_db = db_session.query(
        ProductModel).filter_by(id=product_on_db.id).first()

    assert product_updated_on_db is not None
    assert product_updated_on_db.name == product.name
    assert product_updated_on_db.slug == product.slug
    assert product_updated_on_db.price == product.price
    assert product_updated_on_db.stock == product.stock


def test_update_product_invalid_id(db_session):
    product = Product(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=22
    )

    uc = ProductUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.update_product(id=1, product=product)


def test_delete_product(db_session, product_on_db):
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=product_on_db.id)

    deleted_product = db_session.query(
        ProductModel).filter_by(id=product_on_db.id).first()

    assert deleted_product is None


def test_delete_product_non_exist(db_session):
    uc = ProductUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.delete_product(id=1)


def test_list_products(db_session, products_on_db):
    uc = ProductUseCases(db_session=db_session)

    page = uc.list_products(page=1, size=4)

    assert type(page) == Page
    assert len(page.items) == 4

    assert page.items[0].name == products_on_db[0].name
    assert page.items[0].slug == products_on_db[0].slug
    assert page.items[0].price == products_on_db[0].price
    assert page.items[0].stock == products_on_db[0].stock

    assert page.total == 4
    assert page.page == 1
    assert page.size == 4
    assert page.pages == 1


def test_list_products_with_search(db_session, products_on_db):
    uc = ProductUseCases(db_session=db_session)

    page = uc.list_products(search='nike')

    assert type(page) == Page
