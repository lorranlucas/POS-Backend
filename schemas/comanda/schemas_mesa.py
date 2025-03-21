from pydantic import BaseModel
from typing import Optional, List
from schemas.comanda.schemas_comanda import ComandaSchema  # Ajustado para ComandaSchema

class MesaCreate(BaseModel):
    codg: str
    posicao: int
    tipo: str
    status: str = "livre"
    area: Optional[str] = None
    empresa_id: int

class MesaResponse(BaseModel):
    id: int
    codg: str
    posicao: int
    tipo: str
    status: str
    area: Optional[str] = None
    empresa_id: int
    comandas: List[ComandaSchema] = []  # Ajustado para ComandaSchema

    class Config:
        from_attributes = True  # Atualizado para Pydantic V2