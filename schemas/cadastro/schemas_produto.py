from pydantic import BaseModel, EmailStr
from typing import Optional, List
from decimal import Decimal

# Schema Composicao
class ComposicaoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco_adicional: Optional[Decimal] = None
    tipo: Optional[str] = None

class ComposicaoCreate(ComposicaoBase):
    pass

class Composicao(ComposicaoBase):
    id: int
    id_produto: Optional[int] = None
    empresa_id: int

    class Config:
        from_attributes = True

# Schema EtapaAcompanhamento
class EtapaAcompanhamentoBase(BaseModel):
    id_produto: int
    preco: Optional[Decimal] = None

class EtapaAcompanhamentoCreate(EtapaAcompanhamentoBase):
    pass

class EtapaAcompanhamento(EtapaAcompanhamentoBase):
    id: int
    id_etapa: Optional[int] = None
    empresa_id: int

    class Config:
        from_attributes = True

# Schema Etapa
class EtapaBase(BaseModel):
    nome: str
    posicao: Optional[int] = None

class EtapaCreate(EtapaBase):
    acompanhamentos: Optional[List[EtapaAcompanhamentoCreate]] = []

class Etapa(EtapaBase):
    id: int
    produto_id: Optional[int] = None
    empresa_id: int
    acompanhamentos: List[EtapaAcompanhamento] = []

    class Config:
        from_attributes = True

# Schema Produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    codigo_de_barra: Optional[str] = None
    disponibilidade: Optional[bool] = None
    preco: Optional[Decimal] = None
    id_und_med: Optional[str] = None
    foto: Optional[str] = None
    id_categoria: Optional[int] = None
    id_fornecedor: Optional[int] = None
    id_setor: Optional[int] = None

class ProdutoCreate(ProdutoBase):
    etapas: Optional[List[EtapaCreate]] = []
    composicoes: Optional[List[ComposicaoCreate]] = []

class Produto(ProdutoBase):
    id: int
    empresa_id: int
    etapas: List[Etapa] = []
    composicoes: List[Composicao] = []

    class Config:
        from_attributes = True

