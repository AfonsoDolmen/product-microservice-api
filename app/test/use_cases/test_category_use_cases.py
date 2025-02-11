from sqlalchemy.orm import Session
from typing import List
from app.use_cases.category import CategoryUseCases
from app.db.models import Category as CategoryModel
from app.schemas.category import Category, CategoryOutput
from app.test.conftest import db_session


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

    categories = uc.list_categories(db_session)

    assert len(categories) == 4
    assert type(categories[0]) == CategoryOutput
    assert categories[0].id == categories_on_db[0].id
    assert categories[0].name == categories_on_db[0].name
    assert categories[0].slug == categories_on_db[0].slug
