from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from extensions import Base

class Balcao(Base):
    __tablename__ = 'balcoes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    empresa = relationship('Empresa', back_populates='balcoes')