from sqlalchemy.orm import Session
from models.cadastro.models_geral import Fornecedor
from schemas.cadastro.schemas_fornecedor import FornecedorCreate

class FornecedorService:
    @staticmethod
    def create_fornecedor(db: Session, fornecedor: FornecedorCreate, empresa_id: int):
        db_fornecedor = Fornecedor(**fornecedor.dict(), empresa_id=empresa_id)
        db.add(db_fornecedor)
        db.commit()
        db.refresh(db_fornecedor)
        return db_fornecedor

    @staticmethod
    def get_fornecedores(db: Session, empresa_id: int):
        return db.query(Fornecedor).filter(Fornecedor.empresa_id == empresa_id).all()

    @staticmethod
    def get_fornecedor(db: Session, fornecedor_id: int, empresa_id: int):
        return db.query(Fornecedor).filter(
            Fornecedor.id == fornecedor_id,
            Fornecedor.empresa_id == empresa_id
        ).first()

    @staticmethod
    def update_fornecedor(db: Session, fornecedor_id: int, fornecedor: FornecedorCreate, empresa_id: int):
        db_fornecedor = db.query(Fornecedor).filter(
            Fornecedor.id == fornecedor_id,
            Fornecedor.empresa_id == empresa_id
        ).first()
        if db_fornecedor:
            for key, value in fornecedor.dict().items():
                setattr(db_fornecedor, key, value)
            db.commit()
            db.refresh(db_fornecedor)
        return db_fornecedor

    @staticmethod
    def delete_fornecedor(db: Session, fornecedor_id: int, empresa_id: int):
        db_fornecedor = db.query(Fornecedor).filter(
            Fornecedor.id == fornecedor_id,
            Fornecedor.empresa_id == empresa_id
        ).first()
        if db_fornecedor:
            db.delete(db_fornecedor)
            db.commit()
            return True
        return False