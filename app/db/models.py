from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    """
    Cria a tabela de categorias no banco de dados
    """
    __tablename__ = 'categories'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    slug = Column('slug', String, nullable=False)
    products = relationship('Product', back_populates='category')


class Product(Base):
    """
    Cria a tabela de produtos no banco de dados
    """
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    slug = Column('slug', String, nullable=False)
    price = Column('price', Float)
    stock = Column('stock', Integer)
    created_at = Column('created_at', DateTime, server_default=func.now())
    updated_at = Column('updated_at', DateTime, onupdate=func.now())
    category_id = Column('category_id', ForeignKey(
        'categories.id'), nullable=False)
    category = relationship('Category', back_populates='products')


class User(Base):
    """
    Cria a tabela de usuários no banco de dados
    """
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
