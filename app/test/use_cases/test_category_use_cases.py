import pytest
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.use_cases.category import CategoryUseCases
from app.db.models import Category as CategoryModel
from app.schemas.category import Category, CategoryOutput


def test_add_category_uc(db_session: Session):
    """
    Testando ao adicionar um novo registro no banco
    """
    uc = CategoryUseCases(db_session)

    category = Category(
        name='Roupa',
        slug='roupa'
    )

    uc.add_category(category)

    categories_on_db = db_session.query(CategoryModel).all()

    assert len(categories_on_db) == 1
    assert categories_on_db[0].name == 'Roupa'
    assert categories_on_db[0].slug == 'roupa'

    db_session.delete(categories_on_db[0])
    db_session.commit()


def test_list_categories(db_session: Session, categories_on_db: List[Category]):
    """
    Testando ao listar todos os registros do banco
    """
    uc = CategoryUseCases(db_session)

    categories = uc.list_categories()

    assert len(categories) == 4
    assert type(categories[0]) == CategoryOutput
    assert categories[0].id == categories_on_db[0].id
    assert categories[0].name == categories_on_db[0].name
    assert categories[0].slug == categories_on_db[0].slug


def test_delete_category(db_session: Session):
    """
    Testando ao deletar um registro
    """
    category_model = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category_model)
    db_session.commit()

    uc = CategoryUseCases(db_session=db_session)
    uc.delete_category(id=category_model.id)

    category_model = db_session.query(
        CategoryModel).filter_by(id=category_model.id).first()

    assert category_model is None


def test_delete_category_non_exist(db_session: Session):
    """
    Testando ao deletar um registro que não existe
    """
    uc = CategoryUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.delete_category(id=1)
