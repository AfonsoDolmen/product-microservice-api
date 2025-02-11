from sqlalchemy.orm import Session
from app.db.models import Category as CategoryModel
from app.schemas.category import Category, CategoryOutput


class CategoryUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_category(self, category: Category):
        """
        Adiciona um novo registro no banco
        """
        category_model = CategoryModel(**category.dict())

        self.db_session.add(category_model)
        self.db_session.commit()

    def list_categories(self):
        """
        Lista todos os registros do banco
        """
        categories_on_db = self.db_session.query(CategoryModel).all()
        categories_output = [self.serialize_category(
            category_model) for category_model in categories_on_db]

        return categories_output

    def serialize_category(self, category_model: CategoryModel):
        """
        Serializa a saída para o usuário
        """
        return CategoryOutput(**category_model.__dict__)
