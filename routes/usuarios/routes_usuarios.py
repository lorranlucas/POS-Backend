from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.usuarios.schemas_usuarios import UsuarioCreate, UsuarioResponse, UsuarioLogin
from services.usuarios.services_usuarios import criar_usuario, login_usuario
from extensions import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# Rota de registro de usuário
@router.post("/", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, usuario)

# Rota de login de usuário
@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    return login_usuario(db, usuario)
