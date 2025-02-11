from app.db.connection import Session


def get_db_session():
    """
    Cria e retorna uma nova sessão no banco
    """
    try:
        session = Session()
        yield session
    finally:
        session.close()
