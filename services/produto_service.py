import os
from extensions import db
from flask import current_app
from werkzeug.utils import secure_filename
from models import Produto, Etapa, EtapaAcompanhamento,Composicao,Categoria

import uuid

from werkzeug.datastructures import FileStorage

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/produtos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Certifique-se de criar a pasta de upload
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    
def criar_produto(produto_data):
    print("Dados recebidos: ", produto_data)
    tipo = produto_data.get('tipo')
    if not tipo:
        raise ValueError("O campo 'tipo' é obrigatório.")

    foto = produto_data.get('foto')  # Foto como arquivo

    disponibilidade = produto_data.get('disponibilidade', False)
    if isinstance(disponibilidade, str):
        disponibilidade = disponibilidade.lower() in ['true', '1', 'yes', 'sim']

    novo_produto = Produto(
        nome=produto_data.get('nome'),
        descricao=produto_data.get('descricao'),
        tipo=tipo,
        codigo_de_barra=produto_data.get('codigo_de_barra'),
        disponibilidade=disponibilidade,
        preco=produto_data.get('preco', 0.00),
        id_und_med=produto_data.get('id_und_med'),
        foto=foto,  # Caminho salvo no banco
        id_categoria=produto_data.get('categoria'),
        id_fornecedor=produto_data.get('id_fornecedor'),
        id_setor=produto_data.get('setor')
    )

    db.session.add(novo_produto)
    db.session.commit()
    
    # Agora podemos acessar o novo_produto.id, pois o produto foi persistido e o ID foi gerado
    print(f"Produto criado com ID: {novo_produto.id}")
    
    # Se o produto for do tipo 'combo', processa as etapas e acompanhamentos
    if tipo == 'combo' and 'etapas' in produto_data:
        for etapa_data in produto_data['etapas']:
            etapa = Etapa(
                produto_id=novo_produto.id,  # Atribuindo o produto_id
                nome=etapa_data['nome'],
                posicao=etapa_data['posicao']
            )
            db.session.add(etapa)
            db.session.commit()
            
            if 'acompanhamentos' in etapa_data and isinstance(etapa_data['acompanhamentos'], list):
                for acompanhamento_data in etapa_data['acompanhamentos']:
                    # Verificando se o preço do acompanhamento é válido
                    acompanhamento_preco = acompanhamento_data.get('valor', '')
                    if acompanhamento_preco == '' or not isinstance(acompanhamento_preco, (int, float)):
                        acompanhamento_preco = 0.00  # Defina um valor padrão para preços inválidos ou vazios
                    
                    # Agora associando o id_etapa corretamente
                    acompanhamento = EtapaAcompanhamento(
                        id_etapa=etapa.id,  # Atribuindo o id_etapa da etapa
                        id_produto=acompanhamento_data['id'],
                        preco=acompanhamento_preco
                    )
                    db.session.add(acompanhamento)
                    db.session.commit()

    # Se o produto for do tipo 'composicao', processa as composições
    elif tipo == 'composicao' and 'composicoes' in produto_data:
        for composicao_lista in produto_data['composicoes']:  # Cada item é uma lista, então iteramos sobre elas
            for composicao_data in composicao_lista:  # Iterando sobre a lista interna de composições
                composicao = Composicao(
                    nome=composicao_data['nome'],
                    descricao=composicao_data.get('descricao'),
                    preco_adicional=composicao_data.get('preco_adicional', 0.00),
                    tipo=composicao_data.get('tipo', 'adicional'),
                    id_produto=novo_produto.id
                )
                db.session.add(composicao)
                db.session.commit()
                

    # Commit no banco de dados
    db.session.commit()


from flask import jsonify

def listar_produtos():
    try:
        produtos = Produto.query.all()  # Consulta todos os produtos do banco de dados
        print('produtos',[produto.to_dict() for produto in produtos])
        # Converte os objetos para dicionários e retorna uma lista de dicionários
        return [produto.to_dict() for produto in produtos]
    except Exception as e:
        # Em caso de erro, retorna um dicionário de erro
        return {"error": f"Erro ao listar produtos: {str(e)}"}

def listar_produtos_por_categoria():
    try:
        # Consulta as categorias que têm produtos com disponibilidade True
        categorias = Categoria.query.filter(
            Categoria.produtos.any(Produto.disponibilidade == True)
        ).all()  # Somente categorias com produtos disponíveis
        resultado = []

        for categoria in categorias:
            categoria_dict = categoria.to_dict()  # Converte a categoria em um dicionário
            # Adiciona os produtos dessa categoria que têm disponibilidade True, convertendo-os também para dicionário
            categoria_dict['produtos'] = [
                produto.to_dict() for produto in categoria.produtos if produto.disponibilidade
            ]
            resultado.append(categoria_dict)

        return resultado  # Retorna as categorias que têm produtos com disponibilidade True
    except Exception as e:
        raise Exception(f"Erro ao listar produtos por categoria: {str(e)}")



def listar_produtos_com_etapas_e_acompanhamentos():
    try:

        produtos = Produto.query.all()
        resultado = []
        for produto in produtos:
            produto_dict = produto.to_dict()
            produto_dict['etapas'] = [etapa.to_dict() for etapa in produto.etapas]
            for etapa in produto.etapas:
                etapa_dicts = [acompanhamento.to_dict() for acompanhamento in etapa.acompanhamentos]
                produto_dict['etapas_acompanhamentos'] = etapa_dicts
            resultado.append(produto_dict)
            print(resultado)
        return resultado
    except Exception as e:
        raise Exception(f"Erro ao listar produtos com etapas e acompanhamentos: {str(e)}")

def atualizar_produto(produto_id, produto_data):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")
        
        produto.nome = produto_data.get('nome', produto.nome)
        produto.descricao = produto_data.get('descricao', produto.descricao)
        produto.tipo = produto_data.get('tipo', produto.tipo)
        produto.codigo_de_barra = produto_data.get('codigo_de_barra', produto.codigo_de_barra)
        produto.disponibilidade = produto_data.get('disponibilidade', produto.disponibilidade)
        produto.preco = produto_data.get('preco', produto.preco)
        produto.id_und_med = produto_data.get('id_und_med', produto.id_und_med)
        produto.foto = produto_data.get('foto', produto.foto)

        db.session.commit()
        return produto.to_dict()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar produto: {str(e)}")

def remover_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")
        
        db.session.delete(produto)
        db.session.commit()
        return {"message": "Produto removido com sucesso."}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao remover produto: {str(e)}")

def adicionar_etapa_a_produto(produto_id, etapa_data):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")

        nova_etapa = Etapa(produto_id=produto_id, nome=etapa_data['nome'], posicao=etapa_data['posicao'])
        db.session.add(nova_etapa)
        db.session.commit()
        return nova_etapa.to_dict()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao adicionar etapa ao produto: {str(e)}")

def adicionar_acompanhamento_a_etapa(etapa_id, acompanhamento_data):
    try:
        etapa = Etapa.query.get(etapa_id)
        if not etapa:
            raise Exception("Etapa não encontrada.")
        
        novo_acompanhamento = EtapaAcompanhamento(
            id_etapa=etapa_id,
            id_produto=acompanhamento_data['id_produto'],
            preco=acompanhamento_data.get('preco')
        )
        db.session.add(novo_acompanhamento)
        db.session.commit()
        return novo_acompanhamento.to_dict()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao adicionar acompanhamento à etapa: {str(e)}")

def remover_etapa(etapa_id):
    try:
        etapa = Etapa.query.get(etapa_id)
        if not etapa:
            raise Exception("Etapa não encontrada.")
        
        db.session.delete(etapa)
        db.session.commit()
        return {"message": "Etapa removida com sucesso."}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao remover etapa: {str(e)}")

def remover_acompanhamento(acompanhamento_id):
    try:
        acompanhamento = EtapaAcompanhamento.query.get(acompanhamento_id)
        if not acompanhamento:
            raise Exception("Acompanhamento não encontrado.")
        
        db.session.delete(acompanhamento)
        db.session.commit()
        return {"message": "Acompanhamento removido com sucesso."}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao remover acompanhamento: {str(e)}")
