from fastapi import FastAPI
from config import config
from extensions import Base, engine
from routes.usuarios.routes_empresas import router as empresas_router
from routes.usuarios.routes_usuarios import router as usuarios_router
# Importar os modelos explicitamente
from models.usuarios.models_empresas import Empresa
from models.usuarios.models_licenca import Licenca
from models.usuarios.models_usuario import Usuario
from models.usuarios.models_permissoes import PermissaoUsuario
from models.pedidos.models_balcao import Balcao
from models.usuarios.models_pagamento import Pagamento


from fastapi.middleware.cors import CORSMiddleware

# Cria a aplicação FastAPI
app = FastAPI(
    title="POS Multitenant",
    description="Sistema POS Multitenant com FastAPI",
    debug=config.DEBUG
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Para mais segurança, substitua por ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Incluindo o router para empresas
app.include_router(empresas_router)
app.include_router(usuarios_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao POS Multitenant!"}
