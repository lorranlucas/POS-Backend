from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from extensions import get_db
from models.comandas.models_mesa import Mesa
from schemas.comanda.schemas_mesa import MesaCreate, MesaResponse
from typing import List

router = APIRouter(prefix="/api/mesas", tags=["Mesas"])

@router.post("/", response_model=MesaResponse)
def criar_mesa(mesa_data: MesaCreate, db: Session = Depends(get_db)):
    nova_mesa = Mesa(**mesa_data.dict())
    db.add(nova_mesa)
    db.commit()
    db.refresh(nova_mesa)
    return nova_mesa

@router.get("/{mesa_id}", response_model=MesaResponse)
def obter_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return mesa

@router.get("/", response_model=List[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    mesas = db.query(Mesa).all()
    return mesas