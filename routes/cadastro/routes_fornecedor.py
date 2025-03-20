from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.cadastro.schemas_fornecedor import Fornecedor, FornecedorCreate
from services.cadastro.service_fornecedor import FornecedorService
from extensions import get_db
from models.usuarios.models_empresas import Empresa

router = APIRouter(prefix="/api/fornecedores", tags=["fornecedores"])

async def get_current_empresa(db: Session = Depends(get_db)):
    empresa_id = 1  # Replace with actual token decoding
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=401, detail="Empresa não encontrada")
    return empresa

@router.post("/", response_model=Fornecedor)
async def create_fornecedor(
    fornecedor: FornecedorCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    return FornecedorService.create_fornecedor(db, fornecedor, empresa.id)

@router.get("/", response_model=List[Fornecedor])
async def list_fornecedores(
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    return FornecedorService.get_fornecedores(db, empresa.id)

@router.get("/{fornecedor_id}", response_model=Fornecedor)
async def get_fornecedor(
    fornecedor_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    fornecedor = FornecedorService.get_fornecedor(db, fornecedor_id, empresa.id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@router.put("/{fornecedor_id}", response_model=Fornecedor)
async def update_fornecedor(
    fornecedor_id: int,
    fornecedor: FornecedorCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    updated_fornecedor = FornecedorService.update_fornecedor(db, fornecedor_id, fornecedor, empresa.id)
    if not updated_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return updated_fornecedor

@router.delete("/{fornecedor_id}")
async def delete_fornecedor(
    fornecedor_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    if not FornecedorService.delete_fornecedor(db, fornecedor_id, empresa.id):
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return {"message": "Fornecedor deletado com sucesso"}