from datetime import datetime
import re
import hashlib
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import Base

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    cnpj_cpf = Column(String(18), nullable=False, unique=True)
    email_contato = Column(String(100), nullable=False, unique=True)
    email_personalizado = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(256), nullable=False)
    status = Column(String(20), nullable=False, default='ativo')
    criado_em = Column(DateTime, default=datetime.utcnow)

    licenca = relationship('Licenca', back_populates='empresa', uselist=False, cascade="all, delete-orphan")
    usuarios = relationship('Usuario', back_populates='empresa', cascade="all, delete-orphan")
    balcoes = relationship('Balcao', back_populates='empresa', cascade="all, delete-orphan")

    categorias = relationship("Categoria", backref="empresa", cascade="all, delete-orphan")
    fornecedores = relationship("Fornecedor", backref="empresa", cascade="all, delete-orphan")
    setores = relationship("Setor", backref="empresa", cascade="all, delete-orphan")

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
        if len(valor) == 11:
            if Empresa.validar_cpf(valor):
                return valor
            raise ValueError("CPF inválido")
        elif len(valor) == 14:
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