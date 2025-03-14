from datetime import datetime, timedelta
import uuid
import hashlib
import re
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from dateutil.relativedelta import relativedelta

from app.extensions import Base

# Banco de dados
DATABASE_URL = "mysql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    cnpj_cpf = Column(String(18), nullable=False, unique=True)
    email_contato = Column(String(100), nullable=False, unique=True)
    email_personalizado = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(256), nullable=False)
    status = Column(String(20), nullable=False, default='ativo')  # ativo, inativo, suspenso, cancelado
    criado_em = Column(DateTime, default=datetime.utcnow)

    licenca = relationship('Licenca', back_populates='empresa', uselist=False, cascade="all, delete-orphan")
    usuarios = relationship('Usuario', back_populates='empresa', cascade="all, delete-orphan")
    balcoes = relationship('Balcao', back_populates='empresa', cascade="all, delete-orphan")

    def __init__(self, nome, cnpj_cpf, email_contato, senha):
        self.nome = nome
        self.cnpj_cpf = self.validar_cnpj_cpf(cnpj_cpf)
        self.email_contato = email_contato
        self.senha_hash = generate_password_hash(senha)
        self.email_personalizado = self.gerar_email_personalizado()

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def gerar_email_personalizado(self):
        nome_normalizado = re.sub(r'\s+', '', self.nome.lower())
        nome_normalizado = re.sub(r'[^a-z0-9]', '', nome_normalizado)
        hash_nome = hashlib.md5(nome_normalizado.encode()).hexdigest()[:8]
        return f"{nome_normalizado}_{hash_nome}@simplespdv.com"

    @staticmethod
    def validar_cnpj_cpf(valor):
        valor = re.sub(r'\D', '', valor)
        if len(valor) == 11:  # CPF
            if Empresa.validar_cpf(valor):
                return valor
            raise ValueError("CPF inválido")
        elif len(valor) == 14:  # CNPJ
            if Empresa.validar_cnpj(valor):
                return valor
            raise ValueError("CNPJ inválido")
        raise ValueError("CNPJ/CPF inválido")

    @staticmethod
    def validar_cpf(cpf):
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        def calc_dv(cpf, multiplicador):
            soma = sum(int(cpf[i]) * multiplicador[i] for i in range(len(multiplicador)))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        if calc_dv(cpf, range(10, 1, -1)) == cpf[9] and calc_dv(cpf, range(11, 1, -1)) == cpf[10]:
            return True
        return False

    @staticmethod
    def validar_cnpj(cnpj):
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        def calc_dv(cnpj, pesos):
            soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        if calc_dv(cnpj, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) == cnpj[12] and calc_dv(cnpj, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) == cnpj[13]:
            return True
        return False

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

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(256), nullable=False)
    cargo = Column(String(50), nullable=False, default='funcionario')
    criado_em = Column(DateTime, default=datetime.utcnow)

    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    empresa = relationship('Empresa', back_populates='usuarios')

    permissoes = relationship('PermissaoUsuario', back_populates='usuario', cascade="all, delete-orphan")

    def __init__(self, nome, email, senha, cargo='funcionario'):
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha)
        self.cargo = cargo

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class PermissaoUsuario(Base):
    __tablename__ = 'permissoes_usuario'

    id = Column(Integer, primary_key=True, index=True)
    tela = Column(String(50), nullable=False)
    visualizar = Column(Boolean, default=False)
    editar = Column(Boolean, default=False)
    excluir = Column(Boolean, default=False)
    criar = Column(Boolean, default=False)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='permissoes')

# Funções utilitárias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
