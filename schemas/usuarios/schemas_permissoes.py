from pydantic import BaseModel

class PermissaoUsuarioBase(BaseModel):
    tela: str
    visualizar: bool = False
    editar: bool = False
    excluir: bool = False
    criar: bool = False

class PermissaoUsuarioCreate(PermissaoUsuarioBase):
    pass

class PermissaoUsuario(PermissaoUsuarioBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True