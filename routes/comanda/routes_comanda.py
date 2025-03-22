# routes_comandas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.comanda.schemas_comanda import ComandaCreateSchema, ComandaSchema, ComandaUpdateSchema
from services.comanda.service_comanda import ComandaService
from decimal import Decimal
from extensions import get_db
from pydantic import BaseModel
from models.comandas.models_comadas import Comanda, ItemComanda  # Importação adicionada
from models.cadastro.models_produto import Produto  # Importação adicionada
from sqlalchemy import func, extract

router = APIRouter(prefix="/api/comandas", tags=["Comandas"])

# Schemas existentes
class FormaPagamentoCreateSchema(BaseModel):
    metodo: str
    valor_pago: float

class ComandaStatusUpdateSchema(BaseModel):
    status: str

class ItemStatusProducaoUpdateSchema(BaseModel):
    status_producao: str

# Rotas existentes
@router.post("/", response_model=ComandaSchema)
def create_comanda(comanda: ComandaCreateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        return comanda_service.create_comanda(comanda)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# routes_comandas.py (trecho relevante)
@router.get("/itens/por-mesa-e-balcao", response_model=List[dict], summary="Lista todos os itens por mesa e balcão")
def get_itens_por_mesa_e_balcao(empresa_id: int, db: Session = Depends(get_db)):
    itens = db.query(ItemComanda).join(Comanda).outerjoin(Produto, ItemComanda.produto_id == Produto.id).filter(
        Comanda.empresa_id == empresa_id,
        Comanda.status.in_(["aberta", "paga"]),
        ItemComanda.status_producao != "entregue"  # Exclui itens entregues
    ).all()
    
    resultado = {}
    for item in itens:
        comanda = item.comanda
        chave = f"mesa_{comanda.mesa_id}" if comanda.mesa_id else f"balcao_{comanda.senha}"
        
        if chave not in resultado:
            resultado[chave] = {
                "mesa": comanda.mesa_id if comanda.mesa_id else None,
                "tipo": "mesa" if comanda.mesa_id else "balcao",
                "senha": comanda.senha if comanda.tipo == "balcao" else None,
                "produtos": []
            }
        
        produto_dict = {
            "id": item.id,
            "nome": item.produto.nome if item.produto else "Produto não encontrado",
            "quantidade": item.quantidade,
            "status": item.status_producao
        }
        resultado[chave]["produtos"].append(produto_dict)
    
    return list(resultado.values())


@router.get("/metricas", response_model=dict)
def get_metricas(empresa_id: int, db: Session = Depends(get_db)):
    comandas = db.query(Comanda).filter(Comanda.empresa_id == empresa_id).all()
    
    vendas_totais = sum(float(comanda.valor_total or 0) for comanda in comandas)
    pedidos_realizados = len(comandas)
    clientes_atendidos = len({comanda.mesa_id or comanda.senha for comanda in comandas})
    produtos_vendidos = sum(
        item.quantidade for comanda in comandas for item in comanda.itens
    )

    return {
        "vendas_totais": vendas_totais,
        "pedidos_realizados": pedidos_realizados,
        "clientes_atendidos": clientes_atendidos,
        "produtos_vendidos": produtos_vendidos,
        "vendas_data": [{"value": float(c.valor_total)} for c in comandas[-3:]],
        "pedidos_data": [{"value": len(c.itens)} for c in comandas[-3:]],
        "clientes_data": [{"value": 1 if c.mesa_id or c.senha else 0} for c in comandas[-3:]],
        "produtos_data": [{"value": sum(item.quantidade for item in c.itens)} for c in comandas[-3:]],
    }
@router.get("/metricas/vendas-mensais", response_model=dict)
def get_vendas_mensais(empresa_id: int, db: Session = Depends(get_db)):
    vendas = (
        db.query(
            extract("month", Comanda.data_criacao).label("mes"),
            func.sum(Comanda.valor_total).label("total")
        )
        .filter(Comanda.empresa_id == empresa_id)
        .group_by(extract("month", Comanda.data_criacao))
        .all()
    )
    
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    vendas_por_mes = [0] * 12
    for mes, total in vendas:
        vendas_por_mes[int(mes) - 1] = float(total or 0)

    return {"labels": meses, "data": vendas_por_mes}

@router.get("/metricas/produtos-mais-vendidos", response_model=list)
def get_produtos_mais_vendidos(empresa_id: int, db: Session = Depends(get_db)):
    produtos = (
        db.query(Produto.nome, func.sum(ItemComanda.quantidade).label("total_vendido"))
        .join(ItemComanda, ItemComanda.produto_id == Produto.id)
        .join(Comanda, Comanda.id == ItemComanda.comanda_id)
        .filter(Comanda.empresa_id == empresa_id)
        .group_by(Produto.nome)
        .order_by(func.sum(ItemComanda.quantidade).desc())
        .limit(5)
        .all()
    )
    
    return [{"name": nome, "sales": int(total_vendido)} for nome, total_vendido in produtos]

@router.get("/itens/por-mesa-e-balcao", response_model=List[dict], summary="Lista todos os itens por mesa e balcão")
def get_itens_por_mesa_e_balcao(empresa_id: int, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    itens = db.query(ItemComanda).join(Comanda).join(Produto, ItemComanda.produto_id == Produto.id).filter(
        Comanda.empresa_id == empresa_id,
        Comanda.status.in_(["aberta", "paga"])
    ).all()
    
    resultado = {}
    for item in itens:
        comanda = item.comanda
        chave = f"mesa_{comanda.mesa_id}" if comanda.mesa_id else f"balcao_{comanda.senha}"
        
        if chave not in resultado:
            resultado[chave] = {
                "mesa": comanda.mesa_id if comanda.mesa_id else None,
                "tipo": "mesa" if comanda.mesa_id else "balcao",
                "senha": comanda.senha if comanda.tipo == "balcao" else None,
                "produtos": []
            }
        
        produto_dict = {
            "id": item.id,
            "nome": item.produto.nome,
            "quantidade": item.quantidade,
            "status": item.status_producao
        }
        resultado[chave]["produtos"].append(produto_dict)
    
    return list(resultado.values())

@router.post("/{comanda_id}/pagamento", response_model=ComandaSchema)
def adicionar_forma_pagamento(comanda_id: int, pagamento: FormaPagamentoCreateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        return comanda_service.adicionar_forma_pagamento(comanda_id, pagamento.metodo, Decimal(str(pagamento.valor_pago)))
    except ValueError as e:
        if "Comanda não encontrada" in str(e):
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metricas/vendas-totais", response_model=dict)
def get_vendas_totais(empresa_id: int, db: Session = Depends(get_db)):
    total = db.query(func.sum(Comanda.valor_total)).filter(Comanda.empresa_id == empresa_id).scalar() or 0
    return {"total_vendas": float(total)}

@router.get("/metricas/produtos-vendidos", response_model=list)
def get_produtos_vendidos(empresa_id: int, limit: int = 5, db: Session = Depends(get_db)):
    produtos = (
        db.query(Produto.nome, func.sum(ItemComanda.quantidade).label("total_vendido"))
        .join(ItemComanda, ItemComanda.produto_id == Produto.id)
        .join(Comanda, Comanda.id == ItemComanda.comanda_id)
        .filter(Comanda.empresa_id == empresa_id)
        .group_by(Produto.nome)
        .order_by(func.sum(ItemComanda.quantidade).desc())
        .limit(limit)
        .all()
    )
    return [{"nome": nome, "quantidade": int(total_vendido)} for nome, total_vendido in produtos]

@router.patch("/{comanda_id}", response_model=ComandaSchema)
def update_comanda_status(comanda_id: int, status_data: ComandaStatusUpdateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        return comanda_service.update_comanda_status(comanda_id, status_data.status)
    except ValueError as e:
        if "Comanda não encontrada" in str(e):
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mesa/{mesa_id}/finalizar-comandas")
def finalizar_comandas_mesa(mesa_id: int, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        if not comanda_service.finalizar_comandas_mesa(mesa_id):
            raise HTTPException(status_code=404, detail="Nenhuma comanda encontrada para essa mesa ou todas já estão fechadas")
        return {"message": "Comandas da mesa finalizadas com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/itens/status/{status_producao}", response_model=List[dict])
def get_itens_by_status_producao(status_producao: str, empresa_id: int, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    itens = comanda_service.get_itens_by_status_producao(status_producao, empresa_id)
    return [item.to_dict() for item in itens]

@router.patch("/itens/{item_id}/status-producao", response_model=dict)
def update_item_status_producao(item_id: int, status_data: ItemStatusProducaoUpdateSchema, db: Session = Depends(get_db)):
    comanda_service = ComandaService(db)
    try:
        item = comanda_service.update_item_status_producao(item_id, status_data.status_producao)
        return item.to_dict()
    except ValueError as e:
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