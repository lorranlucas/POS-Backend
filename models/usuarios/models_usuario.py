from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(256), nullable=False)  # Campo para armazenar o hash da senha
    cargo = Column(String(50), nullable=False, default='funcionario')
    criado_em = Column(DateTime, default=datetime.utcnow)

    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    empresa = relationship('Empresa', back_populates='usuarios')

    permissoes = relationship('PermissaoUsuario', back_populates='usuario', cascade="all, delete-orphan")

    def __init__(self, nome, email, senha, cargo='funcionario', empresa_id=None):
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha)
        self.cargo = cargo
        if empresa_id:
            self.empresa_id = empresa_id  # Atribui o ID da empresa, caso seja passado

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
