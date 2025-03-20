from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from extensions import Base

# Modelo Mesa
class Mesa(Base):
    __tablename__ = 'mesa'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codg = Column(String(50), nullable=False)  # Código identificador da mesa
    posicao = Column(Integer, nullable=False)  # Posição da mesa (ex.: número ou ordem no salão)
    tipo = Column(String(50), nullable=False)  # Tipo da mesa (ex.: "quadrada", "retangular", "redonda")
    status = Column(String(50), nullable=False, default="livre")  # Status (ex.: "livre", "ocupada", "reservada")
    area = Column(String(50), nullable=True)  # Área onde a mesa está localizada (ex.: "salão", "varanda")
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    # Relacionamento com Comanda (uma mesa pode ter várias comandas)
    comandas = relationship('Comanda', backref='mesa', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "codg": self.codg,
            "posicao": self.posicao,
            "tipo": self.tipo,
            "status": self.status,
            "area": self.area,
            "empresa_id": self.empresa_id,
            "comandas": [comanda.to_dict() for comanda in self.comandas]
        }

    def __repr__(self):
        return f"<Mesa {self.codg} - Status {self.status}>"