from pydantic import BaseModel, Field, conint
from typing import Optional, List
from model.item import Item
from flask_paginate import Pagination
from flask_sqlalchemy import SQLAlchemy, pagination


class ItemSchema(BaseModel):
    """
    """
    nome: str = Field("Uramaki Salmão", description="Nome do item")
    descricao: str = Field(
        "Roll de salmão crispy com cream cheese e molho tarê", description="Descrição do item")
    quantidade: conint(gt=0) = Field(
        1, description="A quantidade de itens para adicionar na lista")
    valor: float = Field(
        4.99, description="O valor do item em formato de moeda internacional (i.e casas decimais com divisão em .)")
    peso: float = Field(0.14, description="O peso em grama (g) do item")
    status: bool = Field(
        default=True, description="Status do item (ativo/inativo)")
    imagem: Optional[str] = Field(
        None, description="Caminho da imagem do item")


class EditarItemSchema(BaseModel):
    """
    """
    item_id: int = Field(..., title="ID do item",
                         description="O ID do item que deseja editar")

    nome: str = Field("Uramaki Salmão", description="Nome do item")
    descricao: str = Field(
        "Roll de salmão crispy com cream cheese e molho tarê", description="Descrição do item")
    quantidade: conint(gt=0) = Field(
        1, description="A quantidade de itens para adicionar na lista")
    valor: float = Field(
        4.99, description="O valor do item em formato de moeda internacional (i.e casas decimais com divisão em .)")
    peso: float = Field(0.14, description="O peso em grama (g) do item")
    status: bool = Field(
        default=True, description="Status do item (ativo/inativo)")
    imagem: Optional[str] = Field(
        None, description="Caminho da imagem do item")


class BuscaItemSchema(BaseModel):
    """Define como deve retorna a estrutura do objeto consultado através do ID.
    """

    id: int = Field(..., title="ID do item",
                    description="O ID do item alvo do evento.")


class ListagemItemSchema(BaseModel):
    itens: List[ItemSchema]


def apresenta_itens(itens: List[Item]):
    """Lista todos os Itens cadastrados
    """

    resultado = []
    for item in itens:
        item_dict = {
            "id": item.id,
            "nome": item.nome,
            "descricao": item.descricao,
            "quantidade": item.quantidade,
            "peso": item.peso,
            "valor": item.valor,
            "status": item.status,
            "imagem": item.imagem
        }
        # Verifique se o campo 'imagem' do item está vazio
        if item.imagem:
            item_dict["imagem"] = item.imagem
        else:
            # Se estiver vazio, atribua o caminho da imagem padrão
            item_dict["imagem"] = "/uploads/default-image.png"

        resultado.append(item_dict)
    return {'itens': resultado}


def apresenta_itens(itens_query):
    itens = itens_query.all()

    resultado = []
    for item in itens:
        item_dict = {
            "id": item.id,
            "nome": item.nome,
            "descricao": item.descricao,
            "quantidade": item.quantidade,
            "peso": item.peso,
            "valor": item.valor,
            "status": item.status,
        }
        # Verifique se o campo 'imagem' do item está vazio
        if item.imagem:
            item_dict["imagem"] = item.imagem
        else:
            # Se estiver vazio, atribua o caminho da imagem padrão
            item_dict["imagem"] = "/uploads/default-image.png"

        resultado.append(item_dict)

    return {"itens": resultado}


class ItemCatalogoSchema(BaseModel):
    itens: List[ItemSchema]


class ItemViewSchema(BaseModel):
    """Define como um Item será apresentado
    """

    id: int = 1
    nome: str = "Uramaki Salmão"
    quantidade: Optional[int] = 10
    valor: float = 4.99
    peso: Optional[float] = 0.14
    status: Optional[bool] = True
    # Pode adicionar um valor padrão ou deixar como None
    imagem: Optional[str] = None


class ItemDelSchema(BaseModel):
    """Descrição da exclusão
    """

    message: str
    id: int = Field(..., title="ID do item",
                    description="O ID do item que deve ser excluído.")
    # Pode adicionar um valor padrão ou deixar como None
    imagem: Optional[str] = None


def apresenta_item(item: Item):
    """ Retorna a exibição de um item
    """
    item_dict = {
        "id": item.id,
        "nome": item.nome,
        "descricao": item.descricao,
        "quantidade": item.quantidade,
        "peso": item.peso,
        "valor": item.valor,
        "status": item.status,
    }

    # Verifique se o campo 'imagem' do item está vazio
    if item.imagem:
        item_dict["imagem"] = item.imagem
    else:
        # Se estiver vazio, atribua o caminho da imagem padrão
        item_dict["imagem"] = "/uploads/default-image.png"

    return item_dict
