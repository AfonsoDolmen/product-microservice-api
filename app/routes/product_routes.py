from fastapi import (
    APIRouter,
    Query,
    Response,
    Depends,
    status
)
from fastapi_pagination import Page, add_pagination
from sqlalchemy.orm import Session
from typing import List
from app.routes.deps import get_db_session, auth
from app.use_cases.product import ProductUseCases
from app.schemas.product import Product, ProductInput, ProductOutput

router = APIRouter(prefix='/product',
                   tags=['Produtos'], dependencies=[Depends(auth)])


@router.get('/list', status_code=status.HTTP_200_OK, description='Lista todos os produtos', response_model=Page[ProductOutput])
def list_products(
    search: str = '',
    page: int = Query(1, ge=1, description='Página atual'),
    size: int = Query(10, ge=1, description='Quantidade de itens'),
    db_session: Session = Depends(get_db_session)
):
    """
    Rotas para listar todos os produtos
    """
    uc = ProductUseCases(db_session=db_session)

    return uc.list_products(search=search, page=page, size=size)


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Adiciona um novo produto.', response_model=ProductOutput)
def add_product(
    product_input: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    """
    Rota para adicionar novo produto
    """
    uc = ProductUseCases(db_session=db_session)

    response = uc.add_product(
        product=product_input.product,
        category_slug=product_input.category_slug
    )

    return response


@router.put('/update/{id}', status_code=status.HTTP_200_OK, description='Atualiza um produto.', response_model=ProductOutput)
def update_product(
    id: int,
    product: Product,
    db_session: Session = Depends(get_db_session)
):
    """
    Rota para atualizar um produto
    """
    uc = ProductUseCases(db_session=db_session)
    response = uc.update_product(id=id, product=product)

    return response


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, description='Deleta um produto.')
def delete_product(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    """
    Rota para deletar um produto
    """
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


add_pagination(router)
