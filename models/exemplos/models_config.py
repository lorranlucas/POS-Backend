from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base
from models.models_user import Empresa

class Impressora(Base):
    __tablename__ = 'impressora'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey('empresa.id', ondelete='CASCADE'), nullable=False)
    nome = Column(String(255), nullable=False)
    setor = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)  # Exemplo: "Balcão", "Cozinha", "Entrega"

    empresa = relationship('Empresa', back_populates='impressoras')

    def to_dict(self):
        return {
            "id": self.id,
            "empresa_id": self.empresa_id,
            "nome": self.nome,
            "setor": self.setor,
            "tipo": self.tipo
        }

    def __repr__(self):
        return f"<Impressora {self.id} - {self.nome}>"
