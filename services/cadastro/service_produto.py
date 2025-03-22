from sqlalchemy.orm import Session
from models.cadastro.models_produto import Produto, Etapa, EtapaAcompanhamento, Composicao
from models.cadastro.models_geral import Categoria
from schemas.cadastro.schemas_produto import ProdutoCreate, EtapaCreate, ComposicaoCreate, EtapaAcompanhamentoCreate
import os
from fastapi import UploadFile, HTTPException
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/produtos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file: UploadFile) -> str:
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        return file_path
    return None

def criar_produto(db: Session, produto_data: ProdutoCreate, empresa_id: int, foto: UploadFile = None):
    try:
        foto_path = save_file(foto) if foto else None
        db_produto = Produto(
            nome=produto_data.nome,
            descricao=produto_data.descricao,
            tipo=produto_data.tipo,
            codigo_de_barra=produto_data.codigo_de_barra,
            disponibilidade=produto_data.disponibilidade or False,
            disponivel_delivery=produto_data.disponivel_delivery if produto_data.disponivel_delivery is not None else True,  # Novo campo
            preco=produto_data.preco or 0.00,
            id_und_med=produto_data.id_und_med,
            foto=foto_path,
            id_categoria=produto_data.id_categoria,
            id_fornecedor=produto_data.id_fornecedor,
            id_setor=produto_data.id_setor,
            empresa_id=empresa_id
        )
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)

        if produto_data.tipo == 'combo' and produto_data.etapas:
            for etapa_data in produto_data.etapas:
                db_etapa = Etapa(
                    produto_id=db_produto.id,
                    nome=etapa_data.nome,
                    posicao=etapa_data.posicao,
                    empresa_id=empresa_id
                )
                db.add(db_etapa)
                db.commit()
                db.refresh(db_etapa)

                if etapa_data.acompanhamentos:
                    for acomp_data in etapa_data.acompanhamentos:
                        db_acomp = EtapaAcompanhamento(
                            id_etapa=db_etapa.id,
                            id_produto=acomp_data.id_produto,
                            preco=acomp_data.preco or 0.00,
                            empresa_id=empresa_id
                        )
                        db.add(db_acomp)
                        db.commit()

        if produto_data.tipo == 'composicao' and produto_data.composicoes:
            for comp_data in produto_data.composicoes:
                db_comp = Composicao(
                    nome=comp_data.nome,
                    descricao=comp_data.descricao,
                    preco_adicional=comp_data.preco_adicional or 0.00,
                    tipo=comp_data.tipo or 'adicional',
                    id_produto=db_produto.id,
                    empresa_id=empresa_id
                )
                db.add(db_comp)
                db.commit()

        db.commit()
        return db_produto
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {str(e)}")

def listar_produtos(db: Session, empresa_id: int, disponivel_delivery: bool | None = None):
    try:
        query = db.query(Produto).filter(Produto.empresa_id == empresa_id)
        if disponivel_delivery is not None:
            query = query.filter(Produto.disponivel_delivery == disponivel_delivery)
        return query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

def listar_produtos_por_categoria(db: Session, empresa_id: int, disponivel_delivery: bool | None = None):
    try:
        query = db.query(Categoria).filter(Categoria.empresa_id == empresa_id)
        if disponivel_delivery is not None:
            query = query.filter(Categoria.produtos.any(Produto.disponivel_delivery == disponivel_delivery))
        else:
            query = query.filter(Categoria.produtos.any(Produto.disponibilidade == True))
        categorias = query.all()
        resultado = [
            {
                **categoria.to_dict(),
                'produtos': [
                    produto.to_dict() for produto in categoria.produtos 
                    if produto.disponibilidade and (disponivel_delivery is None or produto.disponivel_delivery == disponivel_delivery)
                ]
            }
            for categoria in categorias
        ]
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos por categoria: {str(e)}")

def listar_produtos_com_etapas_e_acompanhamentos(db: Session, empresa_id: int, disponivel_delivery: bool | None = None):
    try:
        query = db.query(Produto).filter(Produto.empresa_id == empresa_id)
        if disponivel_delivery is not None:
            query = query.filter(Produto.disponivel_delivery == disponivel_delivery)
        produtos = query.all()
        return [produto.to_dict() for produto in produtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos com etapas: {str(e)}")

def atualizar_produto(db: Session, produto_id: int, produto_data: ProdutoCreate, empresa_id: int, foto: UploadFile = None):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id, Produto.empresa_id == empresa_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        if foto:
            produto.foto = save_file(foto)

        for key, value in produto_data.dict(exclude_unset=True).items():
            if key not in ['etapas', 'composicoes']:
                setattr(produto, key, value)
        db.commit()
        db.refresh(produto)
        return produto
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar produto: {str(e)}")

def remover_produto(db: Session, produto_id: int, empresa_id: int):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id, Produto.empresa_id == empresa_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        db.delete(produto)
        db.commit()
        return {"message": "Produto removido com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover produto: {str(e)}")

# As funções de etapas e acompanhamentos permanecem inalteradas
def adicionar_etapa_a_produto(db: Session, produto_id: int, etapa_data: EtapaCreate, empresa_id: int):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id, Produto.empresa_id == empresa_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        nova_etapa = Etapa(produto_id=produto_id, nome=etapa_data.nome, posicao=etapa_data.posicao, empresa_id=empresa_id)
        db.add(nova_etapa)
        db.commit()
        db.refresh(nova_etapa)
        return nova_etapa
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar etapa: {str(e)}")

def adicionar_acompanhamento_a_etapa(db: Session, etapa_id: int, acomp_data: EtapaAcompanhamentoCreate, empresa_id: int):
    try:
        etapa = db.query(Etapa).filter(Etapa.id == etapa_id, Etapa.empresa_id == empresa_id).first()
        if not etapa:
            raise HTTPException(status_code=404, detail="Etapa não encontrada")
        novo_acomp = EtapaAcompanhamento(
            id_etapa=etapa_id,
            id_produto=acomp_data.id_produto,
            preco=acomp_data.preco or 0.00,
            empresa_id=empresa_id
        )
        db.add(novo_acomp)
        db.commit()
        db.refresh(novo_acomp)
        return novo_acomp
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar acompanhamento: {str(e)}")

def remover_etapa(db: Session, etapa_id: int, empresa_id: int):
    try:
        etapa = db.query(Etapa).filter(Etapa.id == etapa_id, Etapa.empresa_id == empresa_id).first()
        if not etapa:
            raise HTTPException(status_code=404, detail="Etapa não encontrada")
        db.delete(etapa)
        db.commit()
        return {"message": "Etapa removida com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover etapa: {str(e)}")

def remover_acompanhamento(db: Session, acompanhamento_id: int, empresa_id: int):
    try:
        acompanhamento = db.query(EtapaAcompanhamento).filter(
            EtapaAcompanhamento.id == acompanhamento_id,
            EtapaAcompanhamento.empresa_id == empresa_id
        ).first()
        if not acompanhamento:
            raise HTTPException(status_code=404, detail="Acompanhamento não encontrado")
        db.delete(acompanhamento)
        db.commit()
        return {"message": "Acompanhamento removido com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover acompanhamento: {str(e)}")