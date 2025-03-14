from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base
from models.models_user import Empresa

print("Models Pedidos")

# Mesas
class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)  # Multi-tenancy
    codg = Column(String(10), unique=True, nullable=False)  # Exemplo: MS-0001
    posicao = Column(Integer, nullable=False)
    tipo = Column(String(30), nullable=False)  # Tipo da mesa (quadrada, retangular, etc.)
    status = Column(String(10), nullable=False, default="livre")  # Status da mesa
    area = Column(String(20), nullable=False, default="salao")  

    empresa = relationship("Empresa", back_populates="mesas")
    comandas = relationship("Comanda", back_populates="mesa", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "id_empresa": self.id_empresa,
            "codg": self.codg,
            "posicao": self.posicao,
            "tipo": self.tipo,
            "status": self.status,
            "area": self.area,
            "comandas": [comanda.to_dict() for comanda in self.comandas]
        }

    def __repr__(self):
        return f"<Mesa {self.codg} - {self.status} - {self.area}>"

# Balcão
class Balcao(Base):
    __tablename__ = "balcoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)  # Multi-tenancy
    codg = Column(String(10), unique=True, nullable=False)  # Exemplo: BL-0001

    empresa = relationship("Empresa", back_populates="balcoes")
    comandas = relationship("Comanda", back_populates="balcao", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "id_empresa": self.id_empresa,
            "codg": self.codg,
            "comandas": [comanda.to_dict() for comanda in self.comandas]
        }

    def __repr__(self):
        return f"<Balcao {self.codg}>"

# Comanda
class Comanda(Base):
    __tablename__ = "comandas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)  # Multi-tenancy
    codg = Column(String(10), unique=True, nullable=False)  # Exemplo: MS-0002 ou BL-0001
    status = Column(String(20), default="aberta")
    total = Column(Numeric(10, 2), default=0.00)

    mesa_id = Column(Integer, ForeignKey("mesas.id", ondelete="SET NULL"), nullable=True)
    balcao_id = Column(Integer, ForeignKey("balcoes.id", ondelete="SET NULL"), nullable=True)

    empresa = relationship("Empresa", back_populates="comandas")
    mesa = relationship("Mesa", back_populates="comandas")
    balcao = relationship("Balcao", back_populates="comandas")
    pedidos = relationship("Pedido", back_populates="comanda", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "id_empresa": self.id_empresa,
            "codg": self.codg,
            "status": self.status,
            "total": str(self.total),
            "pedidos": [pedido.to_dict() for pedido in self.pedidos]
        }

    def __repr__(self):
        return f"<Comanda {self.codg}>"

# Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)  # Multi-tenancy
    comanda_id = Column(Integer, ForeignKey("comandas.id", ondelete="CASCADE"), nullable=False)

    empresa = relationship("Empresa", back_populates="pedidos")
    comanda = relationship("Comanda", back_populates="pedidos")

    def to_dict(self):
        return {
            "id": self.id,
            "id_empresa": self.id_empresa,
            "comanda_id": self.comanda_id
        }

    def __repr__(self):
        return f"<Pedido {self.id}>"
