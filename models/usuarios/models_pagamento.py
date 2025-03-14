from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from extensions import Base

class Pagamento(Base):
    __tablename__ = 'pagamentos'

    id = Column(Integer, primary_key=True, index=True)
    valor_pago = Column(Float, nullable=False)
    data_pagamento = Column(DateTime, default=datetime.utcnow)
    licenca_id = Column(Integer, ForeignKey('licencas.id'), nullable=False)

    licenca = relationship('Licenca', back_populates='pagamentos')