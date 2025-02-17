from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.schemas.user import User
from app.use_cases.user import UserUseCases

router = APIRouter(prefix='/user', tags=['Usuários'])


@router.post('/register', status_code=status.HTTP_201_CREATED, description='Registra um novo usuário')
def user_register(
    user: User,
    db_session: Session = Depends(get_db_session)
):
    """
    Rota para registrar um novo usuário no banco
    """
    uc = UserUseCases(db_session=db_session)
    uc.register_user(user=user)

    return Response(status_code=status.HTTP_201_CREATED)
