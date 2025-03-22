from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import json
import os
from pydantic import BaseModel
from schemas.cadastro.schemas_produto import (
    Produto as ProdutoSchema,
    ProdutoCreate,
    Etapa as EtapaSchema,
    EtapaCreate,
    EtapaAcompanhamento as EtapaAcompanhamentoSchema,
    EtapaAcompanhamentoCreate,
)
from services.cadastro.service_produto import (
    criar_produto,
    listar_produtos,
    listar_produtos_por_categoria,
    listar_produtos_com_etapas_e_acompanhamentos,
    atualizar_produto,
    remover_produto,
    adicionar_etapa_a_produto,
    adicionar_acompanhamento_a_etapa,
    remover_etapa,
    remover_acompanhamento,
)
from extensions import get_db
from models.usuarios.models_empresas import Empresa
from models.cadastro.models_produto import Produto  # Importação adicionada

router = APIRouter(prefix="/api/produtos", tags=["produtos"])

# Modelo Pydantic para o retorno dos setores
class SetorSchema(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True

async def get_current_empresa(db: Session = Depends(get_db)) -> Empresa:
    empresa_id = 1  # TODO: Implementar autenticação real
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=401, detail="Empresa não encontrada")
    return empresa

@router.get("/{produto_id}", response_model=ProdutoSchema)
async def get_produto(produto_id: int, db: Session = Depends(get_db)):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")

@router.get("/uploads/{filename}", summary="Serve uma imagem estática")
async def serve_image(filename: str):
    upload_folder = "uploads/produtos"
    file_path = os.path.join(upload_folder, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"Imagem não encontrada em {file_path}")
    return FileResponse(file_path)

@router.post("/", response_model=ProdutoSchema, summary="Cria um novo produto")
async def create_produto(
    produto: str = Form(...),
    foto: UploadFile | None = File(None),
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    try:
        produto_data = ProdutoCreate(**json.loads(produto))
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Formato JSON inválido")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao processar dados do produto: {str(e)}")
    return criar_produto(db, produto_data, empresa.id, foto)

@router.get("/", response_model=List[ProdutoSchema], summary="Lista todos os produtos")
async def get_produtos(
    disponivel_delivery: bool | None = None,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return listar_produtos(db, empresa.id, disponivel_delivery)

@router.get("/por-categoria/", summary="Lista produtos por categoria")
async def get_produtos_por_categoria(
    disponivel_delivery: bool | None = None,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return listar_produtos_por_categoria(db, empresa.id, disponivel_delivery)

@router.get("/com-etapas/", summary="Lista produtos com etapas e acompanhamentos")
async def get_produtos_com_etapas(
    disponivel_delivery: bool | None = None,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return listar_produtos_com_etapas_e_acompanhamentos(db, empresa.id, disponivel_delivery)

@router.put("/{produto_id}", response_model=ProdutoSchema, summary="Atualiza um produto")
async def update_produto(
    produto_id: int,
    produto: str = Form(...),
    foto: UploadFile | None = File(None),
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    try:
        produto_data = ProdutoCreate(**json.loads(produto))
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Formato JSON inválido")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao processar dados do produto: {str(e)}")
    return atualizar_produto(db, produto_id, produto_data, empresa.id, foto)

@router.delete("/{produto_id}", summary="Remove um produto")
async def delete_produto(
    produto_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return remover_produto(db, produto_id, empresa.id)

@router.post("/{produto_id}/etapas/", response_model=EtapaSchema, summary="Adiciona uma etapa a um produto")
async def add_etapa(
    produto_id: int,
    etapa: EtapaCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return adicionar_etapa_a_produto(db, produto_id, etapa, empresa.id)

@router.post("/etapas/{etapa_id}/acompanhamentos/", response_model=EtapaAcompanhamentoSchema, summary="Adiciona um acompanhamento a uma etapa")
async def add_acompanhamento(
    etapa_id: int,
    acompanhamento: EtapaAcompanhamentoCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return adicionar_acompanhamento_a_etapa(db, etapa_id, acompanhamento, empresa.id)

@router.delete("/etapas/{etapa_id}", summary="Remove uma etapa")
async def delete_etapa(
    etapa_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return remover_etapa(db, etapa_id, empresa.id)

@router.delete("/acompanhamentos/{acompanhamento_id}", summary="Remove um acompanhamento")
async def delete_acompanhamento(
    acompanhamento_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    return remover_acompanhamento(db, acompanhamento_id, empresa.id)