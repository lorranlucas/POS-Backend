from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from extensions import Base

class PermissaoUsuario(Base):
    __tablename__ = 'permissoes_usuario'

    id = Column(Integer, primary_key=True, index=True)
    tela = Column(String(50), nullable=False)
    visualizar = Column(Boolean, default=False)
    editar = Column(Boolean, default=False)
    excluir = Column(Boolean, default=False)
    criar = Column(Boolean, default=False)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='permissoes')