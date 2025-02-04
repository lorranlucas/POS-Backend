from extensions import db

# Modelo TabelaLogin
class TabelaLogin(db.Model):
    __tablename__ = 'tabela_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    chave_de_licenca = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    nome_da_empresa = db.Column(db.String(255), nullable=False)
    nivel_de_acesso = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<TabelaLogin {self.nome_completo}>"

# Modelo Categoria
class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }

    def __repr__(self):
        return f"<Categoria {self.nome}>"

# Modelo Fornecedor
class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.Integer)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nome": self.nome,
            "email": self.email
        }

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"

# Modelo Setor
class Setor(db.Model):
    __tablename__ = 'setor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }

    def __repr__(self):
        return f"<Setor {self.nome}>"

# Modelo Produto
# Modelo Produto
class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # "combo", "solo", "composição"
    codigo_de_barra = db.Column(db.String(255))
    disponibilidade = db.Column(db.Boolean)
    preco = db.Column(db.Numeric(10, 2))
    id_und_med = db.Column(db.String(255), nullable=True)
    foto = db.Column(db.String(255), nullable=True)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id', ondelete='CASCADE'))
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id', ondelete='CASCADE'))
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id', ondelete='CASCADE'))

    categoria = db.relationship('Categoria', backref=db.backref('produtos', cascade='all, delete-orphan'))
    fornecedor = db.relationship('Fornecedor', backref=db.backref('produtos', cascade='all, delete-orphan'))
    setor = db.relationship('Setor', backref=db.backref('produtos', cascade='all, delete-orphan'))
    etapas = db.relationship('Etapa', backref='produto', lazy='joined', cascade='all, delete-orphan')  # Mudança para 'joined'
    composicoes = db.relationship('Composicao', backref='produto', lazy='joined', cascade='all, delete-orphan')  # Mudança para 'joined'

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "id_categoria": self.id_categoria,
            "tipo": self.tipo,
            "codigo_de_barra": self.codigo_de_barra,
            "disponibilidade": self.disponibilidade,
            "preco": str(self.preco),
            "id_und_med": self.id_und_med,
            "id_fornecedor": self.id_fornecedor,
            "id_setor": self.id_setor,
            "foto": self.foto,
            "etapas": [etapa.to_dict() for etapa in self.etapas],
            "composicoes": [composicao.to_dict() for composicao in self.composicoes]
        }

    def __repr__(self):
        return f"<Produto {self.nome}>"

# Modelo Composicao
class Composicao(db.Model):
    __tablename__ = 'composicao'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    preco_adicional = db.Column(db.Numeric(10, 2))  # Preço adicional da composição, se houver
    tipo = db.Column(db.String(50))  # "adicional", "opcional", "extra"
    
    # Relacionamento com os produtos
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco_adicional": str(self.preco_adicional),
            "tipo": self.tipo,
        }

    def __repr__(self):
        return f"<Composicao {self.nome}>"

# Modelo Etapa
# Modelo Etapa
# Modelo Etapa
class Etapa(db.Model):
    __tablename__ = 'etapa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    nome = db.Column(db.String(255), nullable=False)
    posicao = db.Column(db.Integer)

    # Relacionamento com os acompanhamentos
    # Alterei o nome do backref para evitar conflitos
    acompanhamentos = db.relationship('EtapaAcompanhamento', backref='etapa_associada', lazy='joined', cascade='all, delete-orphan')

    def to_dict(self):
        # Incluindo os acompanhamentos na conversão para dict
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "nome": self.nome,
            "posicao": self.posicao,
            "acompanhamentos": [acompanhamento.to_dict() for acompanhamento in self.acompanhamentos]
        }

    def __repr__(self):
        return f"<Etapa {self.nome}>"

# Modelo EtapaAcompanhamento# Modelo EtapaAcompanhamento
# Modelo EtapaAcompanhamento
class EtapaAcompanhamento(db.Model):
    __tablename__ = 'etapa_acompanhamento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_etapa = db.Column(db.Integer, db.ForeignKey('etapa.id'))
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    preco = db.Column(db.Numeric(10, 2))

    # Relacionamento com a Etapa
    etapa = db.relationship('Etapa', backref=db.backref('acompanhamentos_etapa', lazy='joined'))
    
    # Relacionamento com o Produto
    produto = db.relationship('Produto', backref=db.backref('etapas_acompanhamento', lazy='joined'))

    def to_dict(self):
        return {
            "id": self.id,
            "id_etapa": self.id_etapa,
            "id_produto": self.id_produto,
            "produto": self.produto.to_dict() if self.produto else None,  # Inclui o produto completo
            "preco": str(self.preco)
        }

    def __repr__(self):
        return f"<EtapaAcompanhamento {self.id}>"


