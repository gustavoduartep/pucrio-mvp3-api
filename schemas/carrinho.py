from pydantic import BaseModel, Field, conint
from typing import Optional, List


class CarrinhoItemSchema(BaseModel):
    item_id: int = Field(description="ID do item no carrinho", example=1)
    nome: str = Field(description="Nome do item", example="Produto A")
    quantidade: int = Field(
        description="Quantidade do item no carrinho", example=2)


class ListagemCarrinhoSchema(BaseModel):
    items: List[CarrinhoItemSchema] = Field(
        description="Itens no carrinho de compras")
