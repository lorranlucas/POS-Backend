from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.usuarios.schemas_licenca import LicencaCreate, LicencaOut
from services.usuarios.services_licencas import criar_licenca
from extensions import get_db

router = APIRouter()

@router.post("/licencas", response_model=LicencaOut)
async def criar_licenca_route(licenca: LicencaCreate, db: Session = Depends(get_db)):
    return criar_licenca(db, licenca.codigo_licenca, licenca.tipo_licenca, licenca.plano)
