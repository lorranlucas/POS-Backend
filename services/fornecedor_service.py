from models import Fornecedor
from extensions import db
# Listar fornecedores com paginação e filtro
def listar_fornecedores(pagina=1, itens_por_pagina=10, filtro=''):
    query = Fornecedor.query.filter(Fornecedor.nome.ilike(f"%{filtro}%"))

    fornecedores_paginados = query.paginate(page=pagina, per_page=itens_por_pagina)

    fornecedores = [
        fornecedor.to_dict() for fornecedor in fornecedores_paginados.items
    ]

    return fornecedores, fornecedores_paginados.total, fornecedores_paginados.pages

# Criar um novo fornecedor
def criar_fornecedor(codigo, nome, email):
    if Fornecedor.query.filter_by(codigo=codigo).first():
        raise ValueError("Fornecedor com este código já existe!")

    novo_fornecedor = Fornecedor(codigo=codigo, nome=nome, email=email)
    db.session.add(novo_fornecedor)
    db.session.commit()

# Atualizar um fornecedor existente
def atualizar_fornecedor(id, codigo, nome, email):
    fornecedor = Fornecedor.query.get(id)
    if not fornecedor:
        raise ValueError("Fornecedor não encontrado!")

    fornecedor.codigo = codigo
    fornecedor.nome = nome
    fornecedor.email = email
    db.session.commit()

# Remover um fornecedor
def remover_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)
    if not fornecedor:
        raise ValueError("Fornecedor não encontrado!")

    db.session.delete(fornecedor)
    db.session.commit()
