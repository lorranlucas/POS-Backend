from pydantic import BaseModel, EmailStr

class FornecedorBase(BaseModel):
    codigo: str
    nome: str
    email: EmailStr

class FornecedorCreate(FornecedorBase):
    pass

class Fornecedor(FornecedorBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True
        from_attributes = True  # Updated for newer Pydantic versions (v2.x)