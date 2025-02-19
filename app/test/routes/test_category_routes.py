from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
from app.db.models import Category as CategoryModel
from app.main import app

headers = {
    'Authorization': 'Bearer token',
}

client = TestClient(app)
client.headers = headers


def test_list_categories_route(categories_on_db):
    """
    Testa a rota para listar categorias
    """
    response = client.get('/api/v1/category/list?page=1&size=10')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'items' in data
    assert len(data['items']) == 4
    assert data['items'][0] == {
        'name': categories_on_db[0].name,
        'slug': categories_on_db[0].slug,
        'id': categories_on_db[0].id,
    }
    assert data['total'] == 4
    assert data['page'] == 1
    assert data['size'] == 10
    assert data['pages'] == 1


def test_add_category_route(db_session: Session):
    """
    Testa a rota de add category
    """
    body = {
        'name': 'Roupa',
        'slug': 'roupa',
    }

    response = client.post('/api/v1/category/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    categories_on_db = db_session.query(CategoryModel).all()

    assert len(categories_on_db) == 1

    db_session.delete(categories_on_db[0])
    db_session.commit()


def test_delete_category(db_session: Session):
    """
    Testa a rota para deleção de uma categoria
    """
    category_model = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category_model)
    db_session.commit()

    response = client.delete(f'/api/v1/category/delete/{category_model.id}')

    assert response.status_code == status.HTTP_200_OK

    category_model = db_session.query(CategoryModel).filter(
        CategoryModel.id == category_model.id).first()

    assert category_model is None
