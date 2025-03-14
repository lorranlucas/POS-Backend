from sqlalchemy.orm import Session
from models.usuarios.models_licenca import Licenca
from datetime import datetime

def criar_licenca(db: Session, codigo_licenca: str, tipo_licenca: str, plano: str):
    db_licenca = Licenca(codigo_licenca=codigo_licenca, tipo_licenca=tipo_licenca,
                         plano=plano, data_inicio=datetime.now(), data_vencimento=datetime(2024, 12, 31))
    db.add(db_licenca)
    db.commit()
    db.refresh(db_licenca)
    return db_licenca
