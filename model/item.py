from sqlalchemy import Boolean, Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from model.base import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column("pk_item", Integer, primary_key=True)
    nome = Column(String(80), unique=True)
    descricao = Column(String(255), nullable=True)
    quantidade = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    status = Column(Boolean, default=True)
    imagem = Column(String(255), nullable=True)

    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, descricao: str, quantidade: int, valor: float, status: Boolean, peso: float, imagem=None, data_criacao: Union[DateTime, None] = None):
        """
        Cria um novo Item

        Arguments:
            nome: Nome do item ou peça
            quantidade: Quantidade de itens do pedido
            valor: Valor unitário do item
            peso: Peso unitário do item
            status: Item ativo ou inativo para venda
            imagem: Imagem do produto
            data_criacao: Data de cadastro do produto

        """

        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor
        self.peso = peso
        self.status = status
        self.imagem = imagem

        if data_criacao:
            self.data_criacao = data_criacao
