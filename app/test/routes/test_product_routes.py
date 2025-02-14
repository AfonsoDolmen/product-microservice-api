from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import status
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
