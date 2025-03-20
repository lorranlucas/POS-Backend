from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schema para Item da Comanda
class ItemComandaBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    acompanhamentos: Optional[str] = None
    status_producao: str = "pendente"
    pago: bool = False

class ItemComandaCreate(ItemComandaBase):
    pass

class ItemComandaResponse(ItemComandaBase):
    id: int
    comanda_id: int
    empresa_id: int

    class Config:
        from_attributes = True

# Schema para Comanda
class ComandaBase(BaseModel):
    tipo: str  # "mesa" ou "balcao"
    mesa_id: Optional[int] = None
    senha: Optional[str] = None
    valor_total: float
    pago: bool = False

class ComandaCreate(ComandaBase):
    empresa_id: int

class ComandaResponse(ComandaBase):
    id: int
    data_criacao: datetime
    empresa_id: int
    itens: List[ItemComandaResponse] = []

    class Config:
        from_attributes = True
