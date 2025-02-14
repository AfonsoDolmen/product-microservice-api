import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from app.main import app

client = TestClient(app)


def test_add_product_route(db_session: Session, categories_on_db: List[CategoryModel]):
    """
    Testa a rota de add product
    """
    body = {
        'category_slug': categories_on_db[0].slug,
        'product': {
            'name': 'Camisa Nike',
            'slug': 'camisa-nike',
            'price': 22.99,
            'stock': 22,
        },
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 1

    db_session.delete(products_on_db[0])
    db_session.commit()


def test_add_product_route_invalid_category_slug(db_session: Session):
    """
    Teste na validação do slug
    """
    body = {
        'category_slug': 'invalid',
        'product': {
            'name': 'Camisa Nike',
            'slug': 'camisa-nike',
            'price': 22.99,
            'stock': 22,
        },
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_update_product_route(db_session: Session, product_on_db):
    body = {
        'name': 'Updated Camisa',
        'slug': 'updated-camisa',
        'price': 100.99,
        'stock': 20
    }

    response = client.put(f'/product/update/{product_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(product_on_db)

    assert product_on_db.name == 'Updated Camisa'
    assert product_on_db.slug == 'updated-camisa'
    assert product_on_db.price == 100.99
    assert product_on_db.stock == 20


def test_update_product_route_invalid_id():
    body = {
        'name': 'Updated Camisa',
        'slug': 'updated-camisa',
        'price': 100.99,
        'stock': 20
    }

    response = client.put('/product/update/1', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_route(db_session, product_on_db):
    response = client.delete(f'/product/delete/{product_on_db.id}')

    assert response.status_code == status.HTTP_200_OK

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_delete_product_route_invalid_id():
    response = client.delete('/product/delete/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_product_route(db_session, products_on_db):
    response = client.get('/product/list')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 4
    assert data[0] == {
        'id': products_on_db[0].id,
        'name': products_on_db[0].name,
        'slug': products_on_db[0].slug,
        'price': products_on_db[0].price,
        'stock': products_on_db[0].stock,
        'category': {
            'name': products_on_db[0].category.name,
            'slug': products_on_db[0].category.slug,
        },
    }
