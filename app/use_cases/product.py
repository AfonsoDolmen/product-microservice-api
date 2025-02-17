from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from app.schemas.product import Product, ProductInput, ProductOutput


class ProductUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_products(self, search: str = ''):
        """
        Lista todos os registros
        """
        products_on_db = self.db_session.query(ProductModel).filter(
            or_(
                ProductModel.name.ilike(f'%{search}%'),
                ProductModel.slug.ilike(f'%{search}%')
            )
        ).all()

        products = [
            self._serialize_product(product_on_db)
            for product_on_db in products_on_db
        ]

        return products

    def add_product(self, product: ProductInput, category_slug: str):
        """
        Adiciona um novo registro
        """
        category = self.db_session.query(CategoryModel).filter(
            CategoryModel.slug == category_slug).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

        product_model = ProductModel(**product.dict())
        product_model.category_id = category.id

        self.db_session.add(product_model)
        self.db_session.commit()

        return self._serialize_product(product_model)

    def update_product(self, id: int, product: Product):
        """
        Atualiza um registro
        """
        product_on_db = self.db_session.query(
            ProductModel).filter_by(id=id).first()

        if product_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

        product_on_db.name = product.name
        product_on_db.slug = product.slug
        product_on_db.price = product.price
        product_on_db.stock = product.stock

        self.db_session.add(product_on_db)
        self.db_session.commit()

        return self._serialize_product(product_on_db)

    def delete_product(self, id: int):
        """
        Deleta um registro
        """
        product_on_db = self.db_session.query(
            ProductModel).filter_by(id=id).first()

        if product_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

        self.db_session.delete(product_on_db)
        self.db_session.commit()

    def _serialize_product(self, product_on_db: ProductModel):
        """
        Serializa a saída para o usuário
        """
        product_dict = product_on_db.__dict__
        product_dict['category'] = product_on_db.category.__dict__

        return ProductOutput(**product_dict)
