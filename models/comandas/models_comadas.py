from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from extensions import Base

print("Models Comanda")

# Modelo Comanda
class Comanda(Base):
    __tablename__ = 'comanda'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)  # "mesa" ou "balcao"
    numero_mesa = Column(Integer, nullable=True)  # Substituído por relações específicas ou código do balcão
    senha = Column(String(10), nullable=True)  # Sequencial para Balcão (ex.: "B001")
    valor_total = Column(Numeric(10, 2), nullable=False)
    valor_pago = Column(Numeric(10, 2), nullable=False, default=0.00)  # Total pago
    pago = Column(Boolean, default=False)  # Será atualizado com base em valor_pago >= valor_total
    status = Column(String(20), nullable=False, default="aberta")  # Nova coluna: "aberta" ou "finalizada"
    data_criacao = Column(DateTime, default=func.now())
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)
    
    mesa_id = Column(Integer, ForeignKey('mesa.id'), nullable=True)  # Vincula à Mesa

    itens = relationship('ItemComanda', backref='comanda', cascade='all, delete-orphan')
    formas_pagamento = relationship('FormaPagamento', backref='comanda', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "mesa_id": self.mesa_id,
            "senha": self.senha,
            "valor_total": str(self.valor_total) if self.valor_total is not None else None,
            "valor_pago": str(self.valor_pago) if self.valor_pago is not None else None,
            "pago": self.pago,
            "status": self.status,  # Adiciona o status ao dicionário
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "empresa_id": self.empresa_id,
            "itens": [item.to_dict() for item in self.itens],
            "formas_pagamento": [forma.to_dict() for forma in self.formas_pagamento]
        }

    def __repr__(self):
        return f"<Comanda {self.id} - {self.tipo} - Status: {self.status} - Total: R${self.valor_total} - Pago: R${self.valor_pago}>"

# Modelo ItemComanda (sem alterações)
class ItemComanda(Base):
    __tablename__ = 'item_comanda'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comanda_id = Column(Integer, ForeignKey('comanda.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    status_producao = Column(String(50), default="pendente")  # "pendente", "em produção", "pronto", "entregue"
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    produto = relationship('Produto', backref='itens_comanda')
    acompanhamentos = relationship('ItemComandaAcompanhamento', backref='item_comanda', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "comanda_id": self.comanda_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": str(self.preco_unitario) if self.preco_unitario is not None else None,
            "status_producao": self.status_producao,
            "empresa_id": self.empresa_id,
            "produto": self.produto.to_dict() if self.produto else None,
            "acompanhamentos": [acompanhamento.to_dict() for acompanhamento in self.acompanhamentos]
        }

    def __repr__(self):
        return f"<ItemComanda {self.id} - Produto {self.produto_id} - Status {self.status_producao}>"

# Modelo ItemComandaAcompanhamento (sem alterações)
class ItemComandaAcompanhamento(Base):
    __tablename__ = 'item_comanda_acompanhamento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_comanda_id = Column(Integer, ForeignKey('item_comanda.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_adicional = Column(Numeric(10, 2), nullable=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    produto = relationship('Produto', backref='acompanhamentos_itens')

    def to_dict(self):
        return {
            "id": self.id,
            "item_comanda_id": self.item_comanda_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_adicional": str(self.preco_adicional) if self.preco_adicional is not None else None,
            "empresa_id": self.empresa_id,
            "produto": self.produto.to_dict() if self.produto else None
        }

    def __repr__(self):
        return f"<ItemComandaAcompanhamento {self.id} - Produto {self.produto_id}>"

# Modelo FormaPagamento (sem alterações)
class FormaPagamento(Base):
    __tablename__ = 'forma_pagamento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comanda_id = Column(Integer, ForeignKey('comanda.id'), nullable=False)
    metodo = Column(String(50), nullable=False)  # "Dinheiro", "Pix", "Debito", "Credito", "Voucher"
    valor_pago = Column(Numeric(10, 2), nullable=False)
    data_pagamento = Column(DateTime, default=func.now())
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "comanda_id": self.comanda_id,
            "metodo": self.metodo,
            "valor_pago": str(self.valor_pago) if self.valor_pago is not None else None,
            "data_pagamento": self.data_pagamento.isoformat() if self.data_pagamento else None,
            "empresa_id": self.empresa_id
        }

    def __repr__(self):
        return f"<FormaPagamento {self.id} - {self.metodo} - R${self.valor_pago}>"