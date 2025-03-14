from sqlalchemy.orm import Session
from models.usuarios.models_usuario import Usuario
from models.usuarios.models_empresas import Empresa
from schemas.usuarios.schemas_usuarios import UsuarioCreate, UsuarioResponse, UsuarioLogin
from fastapi import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os

# Acessar a chave secreta diretamente sem usar dotenv
SECRET_KEY = "sua_chave_secreta_aqui"  # Substitua por sua chave secreta

def criar_usuario(db: Session, usuario_data: UsuarioCreate):
    # Verificar se o e-mail já está cadastrado
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # Verificar se a empresa existe
    empresa = db.query(Empresa).filter(Empresa.id == usuario_data.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=400, detail="Empresa não encontrada.")

    # Criar o usuário com senha criptografada
    senha_hash = generate_password_hash(usuario_data.senha)
    
    novo_usuario = Usuario(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha=senha_hash,  # Armazenando o hash da senha
        cargo=usuario_data.cargo,
        empresa_id=usuario_data.empresa_id  # Aqui passamos apenas o ID da empresa
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return UsuarioResponse(
        id=novo_usuario.id,
        nome=novo_usuario.nome,
        email=novo_usuario.email,
        cargo=novo_usuario.cargo,
        criado_em=novo_usuario.criado_em,
        empresa_id=novo_usuario.empresa_id
    )

def login_usuario(db: Session, usuario_data: UsuarioLogin):
    # Verificar se o e-mail existe
    usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    
    # Verificar se a senha está correta
    if not check_password_hash(usuario.senha, usuario_data.senha):
        raise HTTPException(status_code=400, detail="Credenciais inválidas.")
    
    # Gerar token JWT
    payload = {
        "sub": usuario.id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expiração do token em 1 hora
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}
