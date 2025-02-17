from sqlalchemy.orm import Session
from fastapi import status
from fastapi import HTTPException
from app.db.models import Category as CategoryModel
from app.schemas.category import Category, CategoryOutput


class CategoryUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_categories(self):
        """
        Lista todos os registros
        """
        categories_on_db = self.db_session.query(CategoryModel).all()
        categories_output = [self._serialize_category(
            category_model) for category_model in categories_on_db]

        return categories_output

    def add_category(self, category: Category):
        """
        Adiciona um novo registro
        """
        category_model = CategoryModel(**category.dict())

        self.db_session.add(category_model)
        self.db_session.commit()

        return self._serialize_category(category_model)

    def delete_category(self, id: int):
        """
        Deleta um registro do banco
        """
        category_model = self.db_session.query(
            CategoryModel).filter_by(id=id).first()

        if not category_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

        self.db_session.delete(category_model)
        self.db_session.commit()

    def _serialize_category(self, category_model: CategoryModel):
        """
        Serializa a saída para o usuário
        """
        return CategoryOutput(
            name=category_model.name,
            slug=category_model.slug,
            id=category_model.id
        )
