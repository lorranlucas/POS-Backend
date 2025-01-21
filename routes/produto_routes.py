from flask import Blueprint, request, jsonify
from services.produto_service import (
    criar_produto,
    listar_produtos,
    atualizar_produto,
    remover_produto,
    listar_produtos_com_etapas_e_acompanhamentos,
    adicionar_etapa_a_produto,
    adicionar_acompanhamento_a_etapa,
    remover_etapa,
    remover_acompanhamento,atualizar_produto_completo
)

produto_bp = Blueprint('produto_bp', __name__)

@produto_bp.route('/produto', methods=['POST'])
def criar():
    
        produto_data = request.get_json()
        print('Produto data recebido:', produto_data)  # Adicionando log para ver os dados recebidos

        produto = criar_produto(produto_data)
        return jsonify(produto), 201


@produto_bp.route('/produtos', methods=['GET'])
def listar():
    try:
        produtos = listar_produtos()
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/produto/<int:produto_id>', methods=['PUT'])
def atualizar(produto_id):
    try:
        produto_data = request.get_json()
        produto = atualizar_produto(produto_id, produto_data)
        return jsonify(produto), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/produto/<int:produto_id>', methods=['DELETE'])
def remover(produto_id):
    try:
        mensagem = remover_produto(produto_id)
        return jsonify(mensagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/produtos/com_etapas_e_acompanhamentos', methods=['GET'])
def listar_com_etapas_e_acompanhamentos():
    try:
        produtos = listar_produtos_com_etapas_e_acompanhamentos()
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/produto/<int:produto_id>/etapa', methods=['POST'])
def adicionar_etapa(produto_id):
    try:
        etapa_data = request.get_json()
        etapa = adicionar_etapa_a_produto(produto_id, etapa_data)
        return jsonify(etapa), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/etapa/<int:etapa_id>/acompanhamento', methods=['POST'])
def adicionar_acompanhamento(etapa_id):
    try:
        acompanhamento_data = request.get_json()
        acompanhamento = adicionar_acompanhamento_a_etapa(etapa_id, acompanhamento_data)
        return jsonify(acompanhamento), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/etapa/<int:etapa_id>', methods=['DELETE'])
def remover_etapa(etapa_id):
    try:
        mensagem = remover_etapa(etapa_id)
        return jsonify(mensagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/acompanhamento/<int:acompanhamento_id>', methods=['DELETE'])
def remover_acompanhamento(acompanhamento_id):
    try:
        mensagem = remover_acompanhamento(acompanhamento_id)
        return jsonify(mensagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/produto/<int:produto_id>/completo', methods=['PUT'])
def atualizar_completo(produto_id):
    try:
        produto_data = request.get_json()
        produto = atualizar_produto_completo(produto_id, produto_data)
        return jsonify(produto), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
