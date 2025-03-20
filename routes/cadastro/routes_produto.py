from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import json
import os
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

router = APIRouter(prefix="/api/produtos", tags=["produtos"])

# Dependência para obter a empresa atual (simulada por enquanto)
async def get_current_empresa(db: Session = Depends(get_db)) -> Empresa:
    """
    Obtém a empresa atual com base em um ID fixo (substituir por autenticação real).
    
    Args:
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        Empresa: Objeto da empresa autenticada.

    Raises:
        HTTPException: Se a empresa não for encontrada (401).
    """
    empresa_id = 1  # TODO: Implementar autenticação real (e.g., JWT)
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=401, detail="Empresa não encontrada")
    return empresa

# Rota para servir imagens estáticas
@router.get("/uploads/{filename}", summary="Serve uma imagem estática")
async def serve_image(filename: str):
    """
    Serve uma imagem estática do diretório 'uploads/produtos'.

    Args:
        filename (str): Nome do arquivo da imagem (ex: 'Screenshot_from_2025-03-16_01-35-25.png').

    Returns:
        FileResponse: Imagem solicitada.

    Raises:
        HTTPException: 404 se a imagem não for encontrada.
    """
    upload_folder = "uploads/produtos"  # Diretório onde as imagens estão salvas
    file_path = os.path.join(upload_folder, filename)  # Caminho completo para o arquivo
    print(f"Tentando servir arquivo em: {file_path}")  # Log para depuração

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
    """
    Cria um novo produto com os dados fornecidos.

    Args:
        produto (str): String JSON contendo os dados do produto.
        foto (UploadFile, optional): Imagem do produto.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        ProdutoSchema: Produto criado.

    Raises:
        HTTPException: Se os dados forem inválidos (422).
    """
    print("Dados recebidos do frontend:")
    print(f"produto (string JSON): {produto}")

    try:
        produto_data = ProdutoCreate(**json.loads(produto))
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Formato JSON inválido")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao processar dados do produto: {str(e)}")

    return criar_produto(db, produto_data, empresa.id, foto)

@router.get("/", response_model=List[ProdutoSchema], summary="Lista todos os produtos")
async def get_produtos(
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Retorna a lista de produtos da empresa autenticada.

    Args:
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        List[ProdutoSchema]: Lista de produtos.
    """
    return listar_produtos(db, empresa.id)

@router.get("/por-categoria/", summary="Lista produtos por categoria")
async def get_produtos_por_categoria(
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Retorna os produtos agrupados por categoria.

    Args:
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        List: Produtos agrupados por categoria.
    """
    return listar_produtos_por_categoria(db, empresa.id)

@router.get("/com-etapas/", summary="Lista produtos com etapas e acompanhamentos")
async def get_produtos_com_etapas(
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Retorna produtos com suas etapas e acompanhamentos.

    Args:
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        List: Produtos com detalhes de etapas e acompanhamentos.
    """
    return listar_produtos_com_etapas_e_acompanhamentos(db, empresa.id)

@router.put("/{produto_id}", response_model=ProdutoSchema, summary="Atualiza um produto")
async def update_produto(
    produto_id: int,
    produto: ProdutoCreate,
    foto: UploadFile | None = File(None),
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Atualiza os dados de um produto existente.

    Args:
        produto_id (int): ID do produto a ser atualizado.
        produto (ProdutoCreate): Dados atualizados do produto.
        foto (UploadFile, optional): Nova imagem do produto.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        ProdutoSchema: Produto atualizado.
    """
    return atualizar_produto(db, produto_id, produto, empresa.id, foto)

@router.delete("/{produto_id}", summary="Remove um produto")
async def delete_produto(
    produto_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Remove um produto da empresa autenticada.

    Args:
        produto_id (int): ID do produto a ser removido.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        dict: Mensagem de sucesso.
    """
    return remover_produto(db, produto_id, empresa.id)

@router.post("/{produto_id}/etapas/", response_model=EtapaSchema, summary="Adiciona uma etapa a um produto")
async def add_etapa(
    produto_id: int,
    etapa: EtapaCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Adiciona uma nova etapa a um produto existente.

    Args:
        produto_id (int): ID do produto.
        etapa (EtapaCreate): Dados da etapa.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        EtapaSchema: Etapa criada.
    """
    return adicionar_etapa_a_produto(db, produto_id, etapa, empresa.id)

@router.post("/etapas/{etapa_id}/acompanhamentos/", response_model=EtapaAcompanhamentoSchema, summary="Adiciona um acompanhamento a uma etapa")
async def add_acompanhamento(
    etapa_id: int,
    acompanhamento: EtapaAcompanhamentoCreate,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Adiciona um acompanhamento a uma etapa existente.

    Args:
        etapa_id (int): ID da etapa.
        acompanhamento (EtapaAcompanhamentoCreate): Dados do acompanhamento.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        EtapaAcompanhamentoSchema: Acompanhamento criado.
    """
    return adicionar_acompanhamento_a_etapa(db, etapa_id, acompanhamento, empresa.id)

@router.delete("/etapas/{etapa_id}", summary="Remove uma etapa")
async def delete_etapa(
    etapa_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Remove uma etapa de um produto.

    Args:
        etapa_id (int): ID da etapa a ser removida.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        dict: Mensagem de sucesso.
    """
    return remover_etapa(db, etapa_id, empresa.id)

@router.delete("/acompanhamentos/{acompanhamento_id}", summary="Remove um acompanhamento")
async def delete_acompanhamento(
    acompanhamento_id: int,
    empresa: Empresa = Depends(get_current_empresa),
    db: Session = Depends(get_db),
):
    """
    Remove um acompanhamento de uma etapa.

    Args:
        acompanhamento_id (int): ID do acompanhamento a ser removido.
        empresa (Empresa): Empresa autenticada.
        db (Session): Sessão do banco de dados.

    Returns:
        dict: Mensagem de sucesso.
    """
    return remover_acompanhamento(db, acompanhamento_id, empresa.id)