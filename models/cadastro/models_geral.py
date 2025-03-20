from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from extensions import Base

class Categoria(Base):
    __tablename__ = 'categoria'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "empresa_id": self.empresa_id}

class Fornecedor(Base):
    __tablename__ = 'fornecedor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "codigo": self.codigo, "nome": self.nome, "email": self.email, "empresa_id": self.empresa_id}

class Setor(Base):
    __tablename__ = 'setor'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'empresa_id': self.empresa_id}