from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response,
    status
)
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination
from app.schemas.category import Category, CategoryOutput
from app.routes.deps import get_db_session, auth
from app.use_cases.category import CategoryUseCases

router = APIRouter(prefix='/category',
                   tags=['Categorias'], dependencies=[Depends(auth)])


@router.get('/list', status_code=status.HTTP_200_OK, description='Lista todas as categorias', response_model=Page[CategoryOutput])
def list_categories(
    db_session: Session = Depends(get_db_session),
    page: int = Query(1, ge=1, description='Páginal atual'),
    size: int = Query(10, ge=1, description='Quantidade de itens')
):
    """
    Rota para listar as categorias
    """
    uc = CategoryUseCases(db_session)

    return uc.list_categories(page=page, size=size)


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Adiciona nova categoria', response_model=CategoryOutput)
def add_category(
    category: Category,
    db_session: Session = Depends(get_db_session),
):
    """
    Rota para criar uma nova categoria
    """
    uc = CategoryUseCases(db_session)
    response = uc.add_category(category)

    return response


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, description='Deleta uma categoria')
def delete_category(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    """
    Rota para deletar uma categoria
    """
    uc = CategoryUseCases(db_session=db_session)
    uc.delete_category(id)

    return Response(status_code=status.HTTP_200_OK)


add_pagination(router)
