from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.comanda.schemas_comanda import ComandaCreateSchema, ComandaSchema, ComandaUpdateSchema
from services.comanda.service_comanda import ComandaService
from decimal import Decimal
from extensions import get_db

router = APIRouter(prefix="/api/comandas", tags=["Comandas"])

# Schema para Forma de Pagamento
from pydantic import BaseModel

class FormaPagamentoCreateSchema(BaseModel):
    metodo: str
    valor_pago: float

# Schema para atualização de status
class ComandaStatusUpdateSchema(BaseModel):
    status: str

@router.post("/", response_model=ComandaSchema)
def create_comanda(comanda: ComandaCreateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        return comanda_service.create_comanda(comanda)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{comanda_id}/pagamento", response_model=ComandaSchema)
def adicionar_forma_pagamento(comanda_id: int, pagamento: FormaPagamentoCreateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        return comanda_service.adicionar_forma_pagamento(comanda_id, pagamento.metodo, Decimal(str(pagamento.valor_pago)))
    except ValueError as e:
        if "Comanda não encontrada" in str(e):
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{comanda_id}", response_model=ComandaSchema)
def update_comanda_status(comanda_id: int, status_data: ComandaStatusUpdateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        return comanda_service.update_comanda_status(comanda_id, status_data.status)
    except ValueError as e:
        if "Comanda não encontrada" in str(e):
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ComandaSchema])
def get_comandas(db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    return comanda_service.get_all_comandas()

@router.get("/{comanda_id}", response_model=ComandaSchema)
def get_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    comanda = comanda_service.get_comanda_by_id(comanda_id)
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return comanda

@router.put("/{comanda_id}", response_model=ComandaSchema)
def update_comanda(comanda_id: int, comanda_data: ComandaUpdateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    comanda = comanda_service.update_comanda(comanda_id, comanda_data)
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return comanda

@router.delete("/{comanda_id}")
def delete_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    if not comanda_service.delete_comanda(comanda_id):
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return {"message": "Comanda deletada com sucesso"}