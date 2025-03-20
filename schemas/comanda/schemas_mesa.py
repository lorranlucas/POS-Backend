from pydantic import BaseModel
from typing import List, Optional
from schemas.comanda.schemas_comanda import ComandaResponse  # Importação corrigida

# Schema para Mesa
class MesaBase(BaseModel):
    codg: str
    posicao: int
    tipo: str
    status: str = "livre"
    area: Optional[str] = None

class MesaCreate(MesaBase):
    empresa_id: int

class MesaResponse(MesaBase):
    id: int
    empresa_id: int
    comandas: List[ComandaResponse] = []  # Agora ComandaResponse está corretamente importado

    class Config:
        from_attributes = True
