from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from extensions import get_db
from schemas.comanda.schemas_comanda import ComandaCreate, ComandaResponse, ItemComandaCreate, ItemComandaResponse
from services.comanda.service_comanda import criar_comanda, obter_comanda, adicionar_item_comanda

router = APIRouter(prefix="/comandas", tags=["Comandas"])

@router.post("/", response_model=ComandaResponse)
def route_criar_comanda(comanda_data: ComandaCreate, db: Session = Depends(get_db)):
    return criar_comanda(db, comanda_data)

@router.get("/{comanda_id}", response_model=ComandaResponse)
def route_obter_comanda(comanda_id: int, db: Session = Depends(get_db)):
    return obter_comanda(db, comanda_id)

@router.post("/{comanda_id}/itens", response_model=ItemComandaResponse)
def route_adicionar_item_comanda(comanda_id: int, item_data: ItemComandaCreate, db: Session = Depends(get_db)):
    return adicionar_item_comanda(db, comanda_id, item_data)
