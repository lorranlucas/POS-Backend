from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class LicencaBase(BaseModel):
    tipo: str
    valor: float
    dia_pagamento: int = 1
    subpacotes: Optional[Dict] = None

class LicencaCreate(LicencaBase):
    pass

class Licenca(LicencaBase):
    id: int
    data_ultimo_pagamento: datetime
    data_expiracao: datetime
    tolerancia: int
    codigo_licenca: str
    empresa_id: int

    class Config:
        from_attributes = True  # Atualizado para Pydantic V2

class LicencaOut(LicencaBase):
    id: int
    data_ultimo_pagamento: datetime
    data_expiracao: datetime
    tolerancia: int
    codigo_licenca: str
    empresa_id: int

    class Config:
        from_attributes = True  # Atualizado para Pydantic V2