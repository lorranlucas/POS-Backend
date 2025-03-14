from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from extensions import get_db
from schemas.usuarios.schemas_empresas import EmpresaCreate, EmpresaOut, LoginEmpresa
from services.usuarios.services_empresas import create_empresa, get_empresa, login_empresa

router = APIRouter(prefix="/api/usuarios/empresas", tags=["empresas"])

@router.post("/", response_model=EmpresaOut)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    print(empresa)
    try:
        db_empresa = create_empresa(db, empresa)
        return db_empresa
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{empresa_id}", response_model=EmpresaOut)
def ler_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = get_empresa(db, empresa_id)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

# Endpoint para login da empresa
# Alteração no seu endpoint de login

@router.post("/login", response_model=EmpresaOut)
def login_empresa_route(login_data: LoginEmpresa, db: Session = Depends(get_db)):
    # Passando o db e o objeto login_data diretamente
    db_empresa = login_empresa(db, login_data.documento, login_data.senha)
    
    if not db_empresa:
        raise HTTPException(status_code=401, detail="CNPJ/CPF ou senha inválidos")
    
    return db_empresa

