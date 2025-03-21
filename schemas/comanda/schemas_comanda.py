from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Schema para Produto (usado nos acompanhamentos e itens)
class ProdutoSchema(BaseModel):
    id: int
    nome: str
    preco: Decimal
    tipo: Optional[str] = None

    class Config:
        from_attributes = True

# Schema para Acompanhamento (entrada)
class AcompanhamentoCreateSchema(BaseModel):
    produto_id: int
    quantidade: int

# Schema para Acompanhamento em ItemComanda (saída)
class ItemComandaAcompanhamentoSchema(BaseModel):
    id: Optional[int] = None
    produto_id: int
    quantidade: int = 1
    preco_adicional: Decimal
    produto: Optional[ProdutoSchema] = None

    class Config:
        from_attributes = True

# Schema para ItemComanda (entrada)
class ItemComandaCreateSchema(BaseModel):
    produto_id: int
    quantidade: int
    acompanhamentos: List[AcompanhamentoCreateSchema] = []

# Schema para ItemComanda (saída)
class ItemComandaSchema(BaseModel):
    id: Optional[int] = None
    produto_id: int
    quantidade: int = 1
    preco_unitario: Decimal
    status_producao: str = "pendente"
    acompanhamentos: List[ItemComandaAcompanhamentoSchema] = []

    class Config:
        from_attributes = True

# Schema para Forma de Pagamento (saída)
class FormaPagamentoSchema(BaseModel):
    id: int
    comanda_id: int
    metodo: str
    valor_pago: Decimal
    data_pagamento: Optional[datetime] = None
    empresa_id: int

    class Config:
        from_attributes = True

# Schema para Forma de Pagamento (entrada)
class FormaPagamentoCreateSchema(BaseModel):
    metodo: str
    valor_pago: float

# Schema para Comanda (entrada)
class ComandaCreateSchema(BaseModel):
    tipo: str
    mesa_id: Optional[int] = None
    senha: Optional[str] = None
    empresa_id: int
    itens: List[ItemComandaCreateSchema] = []

# Schema para Comanda (saída)
class ComandaSchema(BaseModel):
    id: int
    tipo: str
    mesa_id: Optional[int] = None
    senha: Optional[str] = None
    valor_total: Decimal
    valor_pago: Decimal
    pago: bool
    status: str  # Adicionado o campo status
    data_criacao: datetime
    empresa_id: int
    itens: List[ItemComandaSchema] = []
    formas_pagamento: List[FormaPagamentoSchema] = []

    class Config:
        from_attributes = True

# Schema para atualização de Comanda
class ComandaUpdateSchema(BaseModel):
    tipo: Optional[str] = None
    mesa_id: Optional[int] = None
    senha: Optional[str] = None
    valor_total: Optional[Decimal] = None
    valor_pago: Optional[Decimal] = None
    pago: Optional[bool] = None
    status: Optional[str] = None  # Adicionado para permitir atualização do status via PUT, se necessário