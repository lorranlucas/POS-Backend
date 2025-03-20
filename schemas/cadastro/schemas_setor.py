from pydantic import BaseModel

class SetorBase(BaseModel):
    nome: str

class SetorCreate(SetorBase):
    pass

class Setor(SetorBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True
        from_attributes = True  # Updated for newer Pydantic versions (v2.x)