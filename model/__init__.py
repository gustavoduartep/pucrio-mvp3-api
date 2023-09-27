from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.item import Item

db_pasta = "db/"

if not os.path.exists(db_pasta):
    os.makedirs(db_pasta)

db_arquivo = 'sqlite:///%s/db.sqlite3' % db_pasta

conexao = create_engine(db_arquivo, echo=False)

Session = sessionmaker(bind=conexao)

if not database_exists(conexao.url):
    create_database(conexao.url)

Base.metadata.create_all(conexao)


