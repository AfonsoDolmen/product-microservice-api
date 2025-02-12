from fastapi import (
    APIRouter,
    Depends,
    Response,
    status
)
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


@router.get('/list', status_code=status.HTTP_200_OK)
def list_categories(
    db_session: Session = Depends(get_db_session)
):
    uc = CategoryUseCases(db_session)

    return uc.list_categories()


@router.delete('/delete/{id}')
def delete_category(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    uc = CategoryUseCases(db_session=db_session)
    uc.delete_category(id)

    return Response(status_code=status.HTTP_200_OK)
