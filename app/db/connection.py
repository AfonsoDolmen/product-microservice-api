from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = getenv('DB_URL')

# Criando nossa engine e sessão do banco
engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
