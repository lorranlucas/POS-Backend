from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.cadastro.schemas_setor import Setor, SetorCreate
from services.cadastro.service_setor import SetorService
from extensions import get_db
from models.usuarios.models_empresas import Empresa

router = APIRouter(prefix="/api/setores", tags=["setores"])

async def get_current_empresa(db: Session = Depends(get_db)):
    empresa_id = 1  # Replace with actual token decoding
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=401, detail="Empresa não encontrada")
    return empresa

@router.post("/", response_model=Setor)
async def create_setor(
    setor: SetorCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    return SetorService.create_setor(db, setor, empresa.id)

@router.get("/", response_model=List[Setor])
async def list_setores(
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    return SetorService.get_setores(db, empresa.id)

@router.get("/{setor_id}", response_model=Setor)
async def get_setor(
    setor_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    setor = SetorService.get_setor(db, setor_id, empresa.id)
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return setor

@router.put("/{setor_id}", response_model=Setor)
async def update_setor(
    setor_id: int,
    setor: SetorCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    updated_setor = SetorService.update_setor(db, setor_id, setor, empresa.id)
    if not updated_setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return updated_setor

@router.delete("/{setor_id}")
async def delete_setor(
    setor_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    if not SetorService.delete_setor(db, setor_id, empresa.id):
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return {"message": "Setor deletado com sucesso"}