from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.cadastro.schemas_categoria import Categoria, CategoriaCreate
from services.cadastro.service_categoria import CategoriaService
from extensions import get_db
from models.usuarios.models_empresas import Empresa

router = APIRouter(prefix="/api/categorias", tags=["categorias"])

# Dependency to get current empresa (placeholder - implement your auth logic)
async def get_current_empresa(db: Session = Depends(get_db)):
    empresa_id = 1  # Replace with actual token decoding
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=401, detail="Empresa não encontrada")
    return empresa

@router.post("/", response_model=Categoria)
async def create_categoria(
    categoria: CategoriaCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    return CategoriaService.create_categoria(db, categoria, empresa.id)

@router.get("/", response_model=List[Categoria])
async def list_categorias(
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
    pagina: int = 1,
    itens_por_pagina: int = 10,
    filtro: str = ""
):
    return CategoriaService.get_categorias(db, empresa.id, pagina, itens_por_pagina, filtro)

@router.get("/{categoria_id}", response_model=Categoria)
async def get_categoria(
    categoria_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    categoria = CategoriaService.get_categoria(db, categoria_id, empresa.id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.put("/{categoria_id}", response_model=Categoria)
async def update_categoria(
    categoria_id: int,
    categoria: CategoriaCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    updated_categoria = CategoriaService.update_categoria(db, categoria_id, categoria, empresa.id)
    if not updated_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return updated_categoria

@router.delete("/{categoria_id}")
async def delete_categoria(
    categoria_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db)
):
    if not CategoriaService.delete_categoria(db, categoria_id, empresa.id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": "Categoria deletada com sucesso"}