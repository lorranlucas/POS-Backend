from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from extensions import Base

print("Models Comanda")

# Modelo Comanda
# Dentro de models_comandas.py
class Comanda(Base):
    __tablename__ = 'comanda'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)  # "mesa" ou "balcao"
    numero_mesa = Column(Integer, nullable=True)  # Substituído por relações específicas ou codigo do balcao
    senha = Column(String(10), nullable=True)  # Sequencial para Balcão (ex.: "01", "02")
    valor_total = Column(Numeric(10, 2), nullable=False)
    pago = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=func.now())
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)
    
    # Novos campos de chave estrangeira
    mesa_id = Column(Integer, ForeignKey('mesa.id'), nullable=True)      # Vincula à Mesa

    itens = relationship('ItemComanda', backref='comanda', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "mesa_id": self.mesa_id,
            "senha": self.senha,
            "valor_total": str(self.valor_total) if self.valor_total is not None else None,
            "pago": self.pago,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "empresa_id": self.empresa_id,
            "itens": [item.to_dict() for item in self.itens]
        }

    def __repr__(self):
        return f"<Comanda {self.id} - {self.tipo}>"# Modelo ItemComanda
    
class ItemComanda(Base):
    __tablename__ = 'item_comanda'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comanda_id = Column(Integer, ForeignKey('comanda.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    acompanhamentos = Column(Text)  # Armazenado como JSON stringificado
    status_producao = Column(String(50), default="pendente")  # "pendente", "em produção", "pronto", "entregue"
    pago = Column(Boolean, default=False)  # Status de pagamento do item
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    produto = relationship('Produto', backref='itens_comanda')

    def to_dict(self):
        return {
            "id": self.id,
            "comanda_id": self.comanda_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": str(self.preco_unitario) if self.preco_unitario is not None else None,
            "acompanhamentos": self.acompanhamentos,
            "status_producao": self.status_producao,
            "pago": self.pago,
            "empresa_id": self.empresa_id,
            "produto": self.produto.to_dict() if self.produto else None
        }

    def __repr__(self):
        return f"<ItemComanda {self.id} - Produto {self.produto_id} - Status {self.status_producao}>"