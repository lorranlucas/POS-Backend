from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True
        from_attributes = True  # Updated for newer Pydantic versions (v2.x)