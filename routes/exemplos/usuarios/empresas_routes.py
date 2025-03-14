from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from services.usuarios.services_empresas import EmpresaService

app = FastAPI()

# Definindo o modelo Pydantic para validar a entrada
class EmpresaCreate(BaseModel):
    nome: str
    cnpj_cpf: str
    email_contato: EmailStr
    senha: str
    tipo_licenca: str = "free"
    dia_pagamento: int = 1  # Padrão: dia 1 do mês se não for enviado

# Endpoint para cadastrar uma empresa
@app.post("/empresas")
async def cadastrar_empresa(empresa: EmpresaCreate):
    """Endpoint para cadastrar uma empresa"""
    nome = empresa.nome
    cnpj_cpf = empresa.cnpj_cpf
    email_contato = empresa.email_contato
    senha = empresa.senha
    tipo_licenca = empresa.tipo_licenca
    dia_pagamento = empresa.dia_pagamento

    if not all([nome, cnpj_cpf, email_contato, senha]):
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios")

    # Chama o serviço para cadastrar a empresa
    return EmpresaService.cadastrar_empresa(nome, cnpj_cpf, email_contato, senha, tipo_licenca, dia_pagamento)

# Endpoint para listar todas as empresas (placeholder)
@app.get("/empresas")
async def listar():
    """Lista todas as empresas"""
    # Aqui você pode implementar a lógica para retornar as empresas cadastradas
    return {"message": "Lista de empresas"}


# Endpoint para buscar uma empresa pelo ID (placeholder)
@app.get("/empresas/{empresa_id}")
async def buscar(empresa_id: int):
    """Busca uma empresa pelo ID"""
    # Aqui você pode implementar a lógica para buscar a empresa pelo ID
    return {"message": f"Empresa com ID {empresa_id}"}
