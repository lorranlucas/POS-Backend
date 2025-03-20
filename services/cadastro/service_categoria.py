from sqlalchemy.orm import Session
from models.cadastro.models_geral import Categoria
from schemas.cadastro.schemas_categoria import CategoriaCreate

class CategoriaService:
    @staticmethod
    def create_categoria(db: Session, categoria: CategoriaCreate, empresa_id: int):
        db_categoria = Categoria(nome=categoria.nome, empresa_id=empresa_id)
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        return db_categoria

    @staticmethod
    def get_categorias(db: Session, empresa_id: int, pagina: int = 1, itens_por_pagina: int = 10, filtro: str = ""):
        query = db.query(Categoria).filter(Categoria.empresa_id == empresa_id)
        if filtro:
            query = query.filter(Categoria.nome.ilike(f"%{filtro}%"))
        return query.offset((pagina - 1) * itens_por_pagina).limit(itens_por_pagina).all()

    @staticmethod
    def get_categoria(db: Session, categoria_id: int, empresa_id: int):
        return db.query(Categoria).filter(
            Categoria.id == categoria_id,
            Categoria.empresa_id == empresa_id
        ).first()

    @staticmethod
    def update_categoria(db: Session, categoria_id: int, categoria: CategoriaCreate, empresa_id: int):
        db_categoria = db.query(Categoria).filter(
            Categoria.id == categoria_id,
            Categoria.empresa_id == empresa_id
        ).first()
        if db_categoria:
            db_categoria.nome = categoria.nome
            db.commit()
            db.refresh(db_categoria)
        return db_categoria

    @staticmethod
    def delete_categoria(db: Session, categoria_id: int, empresa_id: int):
        db_categoria = db.query(Categoria).filter(
            Categoria.id == categoria_id,
            Categoria.empresa_id == empresa_id
        ).first()
        if db_categoria:
            db.delete(db_categoria)
            db.commit()
            return True
        return False