from sqlalchemy.orm import Session
from models.cadastro.models_geral import Setor
from schemas.cadastro.schemas_setor import SetorCreate

class SetorService:
    @staticmethod
    def create_setor(db: Session, setor: SetorCreate, empresa_id: int):
        db_setor = Setor(nome=setor.nome, empresa_id=empresa_id)
        db.add(db_setor)
        db.commit()
        db.refresh(db_setor)
        return db_setor

    @staticmethod
    def get_setores(db: Session, empresa_id: int):
        return db.query(Setor).filter(Setor.empresa_id == empresa_id).all()

    @staticmethod
    def get_setor(db: Session, setor_id: int, empresa_id: int):
        return db.query(Setor).filter(
            Setor.id == setor_id,
            Setor.empresa_id == empresa_id
        ).first()

    @staticmethod
    def update_setor(db: Session, setor_id: int, setor: SetorCreate, empresa_id: int):
        db_setor = db.query(Setor).filter(
            Setor.id == setor_id,
            Setor.empresa_id == empresa_id
        ).first()
        if db_setor:
            db_setor.nome = setor.nome
            db.commit()
            db.refresh(db_setor)
        return db_setor

    @staticmethod
    def delete_setor(db: Session, setor_id: int, empresa_id: int):
        db_setor = db.query(Setor).filter(
            Setor.id == setor_id,
            Setor.empresa_id == empresa_id
        ).first()
        if db_setor:
            db.delete(db_setor)
            db.commit()
            return True
        return False