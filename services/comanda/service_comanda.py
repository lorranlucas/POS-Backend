from sqlalchemy.orm import Session
from models.comandas.models_comadas import Comanda, ItemComanda
from schemas.comanda.schemas_comanda import ComandaCreate, ComandaResponse, ItemComandaCreate, ItemComandaResponse
from fastapi import HTTPException

def criar_comanda(db: Session, comanda_data: ComandaCreate) -> ComandaResponse:
    nova_comanda = Comanda(**comanda_data.dict())
    db.add(nova_comanda)
    db.commit()
    db.refresh(nova_comanda)
    return nova_comanda

def obter_comanda(db: Session, comanda_id: int) -> ComandaResponse:
    comanda = db.query(Comanda).filter(Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return comanda

def adicionar_item_comanda(db: Session, comanda_id: int, item_data: ItemComandaCreate) -> ItemComandaResponse:
    comanda = db.query(Comanda).filter(Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    novo_item = ItemComanda(**item_data.dict(), comanda_id=comanda_id)
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item
