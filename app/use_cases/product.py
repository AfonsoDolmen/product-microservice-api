from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from app.schemas.product import ProductInput


class ProductUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_product(self, product: ProductInput, category_slug: str):
        category = self.db_session.query(CategoryModel).filter_by(
            slug=category_slug).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

        product_model = ProductModel(**product.dict())
        product_model.category_id = category.id

        self.db_session.add(product_model)
        self.db_session.commit()
