from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_MODE = bool(getenv('TEST_MODE'))
DB_URL = getenv('DB_URL') if TEST_MODE is False else getenv('DB_TEST_URL')

# Criando nossa engine e sessão do banco
engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
