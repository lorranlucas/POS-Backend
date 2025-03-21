from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from extensions import Base
# Em um novo arquivo models_estoque.py ou no mesmo models_produto.py
class Estoque(Base):
    __tablename__ = 'estoque'
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)  # Quantidade em estoque
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    produto = relationship('Produto', backref='estoque')

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade": str(self.quantidade) if self.quantidade is not None else None,
            "empresa_id": self.empresa_id
        }

    def __repr__(self):
        return f"<Estoque {self.produto_id} - Quantidade {self.quantidade}>"