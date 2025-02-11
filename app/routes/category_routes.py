from fastapi import APIRouter, Response, status
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.category import Category
from app.routes.deps import get_db_session
from app.use_cases.category import CategoryUseCases

router = APIRouter(prefix='/category', tags=['Category'])


@router.post('/add', status_code=status.HTTP_201_CREATED)
def add_category(
    category: Category,
    db_session: Session = Depends(get_db_session),
):
    """
    Rota para criar uma nova categoria
    """
    uc = CategoryUseCases(db_session)
    uc.add_category(category)

    return category
