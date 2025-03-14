from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base
from models.models_user import Empresa

# 🔹 Modelo de Categoria
class Categoria(Base):
    __tablename__ = 'categoria'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete="CASCADE"), nullable=False)

    empresa = relationship("Empresa", backref="categorias", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "empresa_id": self.empresa_id
        }

    def __repr__(self):
        return f"<Categoria {self.id} - {self.nome}>"

# 🔹 Modelo de Fornecedor
class Fornecedor(Base):
    __tablename__ = 'fornecedor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False)  
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete="CASCADE"), nullable=False)

    empresa = relationship("Empresa", backref="fornecedores", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nome": self.nome,
            "email": self.email,
            "empresa_id": self.empresa_id
        }

    def __repr__(self):
        return f"<Fornecedor {self.id} - {self.nome}>"

# 🔹 Modelo de Setor
class Setor(Base):
    __tablename__ = 'setor'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete="CASCADE"), nullable=False)

    empresa = relationship("Empresa", backref="setores", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'empresa_id': self.empresa_id
        }

    def __repr__(self):
        return f"<Setor {self.id} - {self.nome}>"
