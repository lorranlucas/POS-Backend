from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from extensions import Base

print("Models Produto")

# Modelo Produto
class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    tipo = Column(String(50))  # "combo", "solo", "composição"
    codigo_de_barra = Column(String(255))
    disponibilidade = Column(Boolean)
    preco = Column(Numeric(10, 2))
    id_und_med = Column(String(255), nullable=True)
    foto = Column(String(255), nullable=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    id_categoria = Column(Integer, ForeignKey('categoria.id', ondelete='CASCADE'))
    id_fornecedor = Column(Integer, ForeignKey('fornecedor.id', ondelete='CASCADE'))
    id_setor = Column(Integer, ForeignKey('setor.id', ondelete='CASCADE'))

    categoria = relationship('Categoria', backref='produtos')
    fornecedor = relationship('Fornecedor', backref='produtos')
    setor = relationship('Setor', backref='produtos')
    etapas = relationship('Etapa', backref='produto', lazy='joined', cascade='all, delete-orphan')
    composicoes = relationship('Composicao', backref='produto', lazy='joined', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "id_categoria": self.id_categoria,
            "tipo": self.tipo,
            "codigo_de_barra": self.codigo_de_barra,
            "disponibilidade": self.disponibilidade,
            "preco": str(self.preco) if self.preco is not None else None,
            "id_und_med": self.id_und_med,
            "id_fornecedor": self.id_fornecedor,
            "id_setor": self.id_setor,
            "foto": self.foto,
            "empresa_id": self.empresa_id,
            "etapas": [etapa.to_dict() for etapa in self.etapas],
            "composicoes": [composicao.to_dict() for composicao in self.composicoes]
        }

    def __repr__(self):
        return f"<Produto {self.nome}>"

# Modelo Composicao
class Composicao(Base):
    __tablename__ = 'composicao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    preco_adicional = Column(Numeric(10, 2))  # Preço adicional da composição, se houver
    tipo = Column(String(50))  # "adicional", "opcional", "extra"
    id_produto = Column(Integer, ForeignKey('produto.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco_adicional": str(self.preco_adicional) if self.preco_adicional is not None else None,
            "tipo": self.tipo,
            "id_produto": self.id_produto,
            "empresa_id": self.empresa_id
        }

    def __repr__(self):
        return f"<Composicao {self.nome}>"

# Modelo Etapa
class Etapa(Base):
    __tablename__ = 'etapa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey('produto.id'))
    nome = Column(String(255), nullable=False)
    posicao = Column(Integer)
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    acompanhamentos = relationship('EtapaAcompanhamento', backref='etapa_associada', lazy='joined', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "nome": self.nome,
            "posicao": self.posicao,
            "empresa_id": self.empresa_id,
            "acompanhamentos": [acompanhamento.to_dict() for acompanhamento in self.acompanhamentos]
        }

    def __repr__(self):
        return f"<Etapa {self.nome}>"

# Modelo EtapaAcompanhamento
class EtapaAcompanhamento(Base):
    __tablename__ = 'etapa_acompanhamento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_etapa = Column(Integer, ForeignKey('etapa.id'))
    id_produto = Column(Integer, ForeignKey('produto.id'))
    preco = Column(Numeric(10, 2))
    empresa_id = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    etapa = relationship('Etapa', backref='acompanhamentos_etapa')
    produto = relationship('Produto', backref='etapas_acompanhamento')

    def to_dict(self):
        return {
            "id": self.id,
            "id_etapa": self.id_etapa,
            "id_produto": self.id_produto,
            "preco": str(self.preco) if self.preco is not None else None,
            "empresa_id": self.empresa_id,
            "produto": self.produto.to_dict() if self.produto else None
        }

    def __repr__(self):
        return f"<EtapaAcompanhamento {self.id}>"