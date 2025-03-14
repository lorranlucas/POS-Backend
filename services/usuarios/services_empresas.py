from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from models.usuarios.models_empresas import Empresa
from models.usuarios.models_licenca import Licenca
from schemas.usuarios.schemas_empresas import EmpresaCreate
from schemas.usuarios.schemas_licenca import LicencaOut

# Valores fixos das licenças definidos pelo provedor
VALORES_LICENCAS = {
    "free": 0.0,
    "starter": 99.90,
    "lite": 199.90,
    "pro": 399.90
}
def create_empresa(db: Session, empresa: EmpresaCreate) -> Empresa:
    # Valida o tipo de licença
    if empresa.tipo_licenca not in VALORES_LICENCAS:
        raise HTTPException(status_code=400, detail="Tipo de licença inválido. Opções: free, starter, lite, pro")
    
    # Cria a empresa
    db_empresa = Empresa(
        nome=empresa.nome,
        cnpj_cpf=empresa.cnpj_cpf,
        email_contato=empresa.email_contato,
        senha=empresa.senha
    )
    
    try:
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
    except IntegrityError as e:
        # Verifica se o erro é relacionado ao campo cnpj_cpf (duplicidade)
        if 'cnpj_cpf' in str(e.orig):
            raise HTTPException(status_code=409, detail="CNPJ/CPF já cadastrado")
        else:
            raise HTTPException(status_code=400, detail="Erro ao criar empresa")

    # Cria a licença associada
    valor_licenca = VALORES_LICENCAS[empresa.tipo_licenca]
    db_licenca = Licenca(
        tipo=empresa.tipo_licenca,
        valor=valor_licenca,
        dia_pagamento=empresa.dia_pagamento
    )
    db_licenca.empresa_id = db_empresa.id
    
    try:
        db.add(db_licenca)
        db.commit()
        db.refresh(db_licenca)
    except IntegrityError as e:
        # Caso a inserção da licença falhe, podemos voltar atrás
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar licença para a empresa")
    
    return db_empresa

def get_empresa(db: Session, empresa_id: int) -> Empresa:
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()



def login_empresa(db: Session, documento: str, senha: str):
    # Tente localizar a empresa pelo CNPJ/CPF
    db_empresa = db.query(Empresa).filter(Empresa.cnpj_cpf == documento).first()

    if db_empresa is None:
        # Se não encontrar a empresa, retorna erro específico
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # Verifica se a senha bate com o hash
    if not db_empresa.verificar_senha(senha):
        # Senha incorreta
        raise HTTPException(status_code=401, detail="Senha incorreta")

    return db_empresa
