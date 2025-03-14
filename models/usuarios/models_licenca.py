from datetime import datetime, timedelta
import uuid
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from dateutil.relativedelta import relativedelta
from extensions import Base

class Licenca(Base):
    __tablename__ = 'licencas'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), nullable=False, default='free')
    subpacotes = Column(JSON, nullable=True)
    valor = Column(Float, nullable=False, default=0.0)
    data_ultimo_pagamento = Column(DateTime, nullable=False, default=datetime.utcnow)
    data_expiracao = Column(DateTime, nullable=False)
    tolerancia = Column(Integer, default=3)
    codigo_licenca = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    dia_pagamento = Column(Integer, nullable=False, default=1)

    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    empresa = relationship('Empresa', back_populates='licenca')

    pagamentos = relationship('Pagamento', back_populates='licenca', cascade="all, delete-orphan")

    def __init__(self, tipo, valor, dia_pagamento=1, subpacotes=None):
        self.tipo = tipo
        self.valor = valor
        self.dia_pagamento = dia_pagamento
        self.subpacotes = subpacotes or {}
        self.atualizar_datas()

    def calcular_proximo_pagamento(self):
        hoje = datetime.utcnow()
        proximo_mes = hoje + relativedelta(months=1)
        return datetime(proximo_mes.year, proximo_mes.month, self.dia_pagamento)

    def atualizar_datas(self):
        if self.tipo == 'free':
            self.data_expiracao = datetime.utcnow() + timedelta(days=7)
        else:
            self.data_expiracao = self.calcular_proximo_pagamento()

    def renovar_licenca(self, valor_pago):
        if valor_pago >= self.valor:
            self.data_ultimo_pagamento = datetime.utcnow()
            self.data_expiracao = self.calcular_proximo_pagamento()
            return True
        return False

    def verificar_licenca_valida(self):
        hoje = datetime.utcnow()
        if self.data_expiracao >= hoje:
            return True
        elif self.data_expiracao + timedelta(days=self.tolerancia) >= hoje:
            return "período de tolerância"
        return False