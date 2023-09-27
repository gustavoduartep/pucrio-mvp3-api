from pydantic import BaseModel, Field


class SuccessSchema(BaseModel):
    message: str = Field(description="Mensagem de sucesso da operação",
                         example="Item adicionado ao carrinho com sucesso")
