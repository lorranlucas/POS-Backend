from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    cargo: Optional[str] = "funcionario"

class UsuarioCreate(UsuarioBase):
    senha: str
    empresa_id: int  # O ID da empresa à qual o usuário pertence

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: datetime
    empresa_id: int

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str
