from fastapi import FastAPI
from config import config
from extensions import Base, engine
from routes.usuarios.routes_empresas import router as empresas_router
from routes.usuarios.routes_usuarios import router as usuarios_router

from routes.cadastro.routes_setor import router as setor_router
from routes.cadastro.routes_categoria import router as categoria_router
from routes.cadastro.routes_fornecedor import router as fornecedor_router
from routes.cadastro.routes_produto import router as produto_router
from routes.comanda.routes_mesa import router as mesa_router
from routes.comanda.routes_comanda import router as comanda_router


# Importar os modelos explicitamente
from models.usuarios.models_empresas import Empresa
from models.usuarios.models_licenca import Licenca
from models.usuarios.models_usuario import Usuario
from models.usuarios.models_permissoes import PermissaoUsuario
from models.pedidos.models_balcao import Balcao
from models.usuarios.models_pagamento import Pagamento
from models.cadastro.models_geral import Fornecedor,Categoria,Setor
from models.comandas.models_comadas import Comanda, ItemComanda
from models.comandas.models_mesa import Mesa




from models.cadastro.models_produto import *



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
app.include_router(setor_router)
app.include_router(categoria_router)
app.include_router(fornecedor_router)
app.include_router(produto_router)

app.include_router(mesa_router)
app.include_router(comanda_router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao POS Multitenant!"}
