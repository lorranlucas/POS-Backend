from pydantic import BaseModel
from datetime import datetime

class EmpresaBase(BaseModel):
    nome: str
    cnpj_cpf: str
    email_contato: str

class EmpresaCreate(EmpresaBase):
    senha: str
    tipo_licenca: str  # free, starter, lite, pro
    dia_pagamento: int  # Dia do mês para pagamento (ex.: 2)

class EmpresaOut(EmpresaBase):
    id: int
    email_personalizado: str
    status: str
    criado_em: datetime

    class Config:
        from_attributes = True

class LoginEmpresa(BaseModel):
    documento: str
    senha: str
