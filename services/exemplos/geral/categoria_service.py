from models.models_geral import Categoria
from app.extensions import db
# Listar categorias com paginação e filtro
def listar_categorias(pagina=1, itens_por_pagina=10, filtro=''):
    query = Categoria.query

    # Aplicar filtro, se fornecido
    if filtro:
        query = query.filter(Categoria.nome.ilike(f"%{filtro}%"))  # Usando 'nome'

    categorias_paginadas = query.paginate(page=pagina, per_page=itens_por_pagina)

    categorias = [
        {"id": categoria.id, "nome": categoria.nome}  # Garantindo que usamos 'nome'
        for categoria in categorias_paginadas.items
    ]

    return categorias, categorias_paginadas.total, categorias_paginadas.pages

# Criar uma nova categoria
def criar_categoria(nome_categoria):
    if Categoria.query.filter_by(nome=nome_categoria).first():
        raise ValueError("A categoria já existe!")

    nova_categoria = Categoria(nome=nome_categoria)
    db.session.add(nova_categoria)
    db.session.commit()

# Atualizar uma categoria existente
def atualizar_categoria(id, novo_nome):
    categoria = Categoria.query.get(id)
    if not categoria:
        raise ValueError("Categoria não encontrada!")

    categoria.nome = novo_nome
    db.session.commit()

# Remover uma categoria
def remover_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        raise ValueError("Categoria não encontrada!")

    db.session.delete(categoria)
    db.session.commit()
