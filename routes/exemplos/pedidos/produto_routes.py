from flask import Blueprint, request, jsonify
from services.pedidos.produto_service import (
    criar_produto,
    listar_produtos,
    atualizar_produto,
    remover_produto,
    listar_produtos_com_etapas_e_acompanhamentos,
    adicionar_etapa_a_produto,
    adicionar_acompanhamento_a_etapa,
    remover_etapa,
    remover_acompanhamento,
    listar_produtos_por_categoria
    #atualizar_produto_completo
)

import os
import base64
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from services.pedidos.produto_service import criar_produto
import os
import json
from flask import send_from_directory
import os

produto_bp = Blueprint('produto_bp', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@produto_bp.route('/uploads/<filename>')
def serve_image(filename):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Rota para criar um produto
@produto_bp.route('/produto', methods=['POST'])
def criar_produto_endpoint():
    try:
        # Processa os dados enviados no formulário
        produto_data = request.form.to_dict()
        etapas = request.form.get('etapas')
        composicoes = request.form.get('composicoes')

        # Se etapas e composições forem enviados como JSON no formulário, converte para objetos Python
        if etapas:
            produto_data['etapas'] = json.loads(etapas)
        if composicoes:
            produto_data['composicoes'] = json.loads(composicoes)

        # Processa o arquivo (foto)
        if 'foto' in request.files:
            file = request.files['foto']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)  # Garante que a pasta exista
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                produto_data['foto'] = file_path  # Adiciona o caminho do arquivo nos dados do produto
            else:
                return jsonify({"error": "Arquivo inválido ou tipo não permitido"}), 400

        # Log para verificar os dados recebidos
        print('Produto data recebido:', produto_data)

        # Chama o serviço para criar o produto
        produto = criar_produto(produto_data)
        return jsonify(produto), 201
    except Exception as e:
        print(f"Erro ao criar produto: {e}")
        return jsonify({"error": str(e)}), 400

@produto_bp.route('/produtos-por-categoria', methods=['GET'])
def produtos_por_categoria():
    produtos = listar_produtos_por_categoria()
    print("produtos_por_categoria",produtos)
    return jsonify(produtos)

# Rota para listar todos os produtos
@produto_bp.route('/produtos', methods=['GET'])
def listar():
    try:
        produtos = listar_produtos()
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para atualizar um produto
@produto_bp.route('/produto/<int:produto_id>', methods=['PUT'])
def atualizar(produto_id):
    try:
        produto_data = request.get_json()
        produto = atualizar_produto(produto_id, produto_data)
        return jsonify(produto), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para remover um produto
@produto_bp.route('/produto/<int:produto_id>', methods=['DELETE'])
def remover(produto_id):
    try:
        mensagem = remover_produto(produto_id)
        return jsonify(mensagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para listar produtos com etapas e acompanhamentos
@produto_bp.route('/produtos/com_etapas_e_acompanhamentos', methods=['GET'])
def listar_com_etapas_e_acompanhamentos():
    try:
        produtos = listar_produtos_com_etapas_e_acompanhamentos()
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para adicionar uma etapa a um produto
@produto_bp.route('/produto/<int:produto_id>/etapa', methods=['POST'])
def adicionar_etapa(produto_id):
    try:
        etapa_data = request.get_json()
        etapa = adicionar_etapa_a_produto(produto_id, etapa_data)
        return jsonify(etapa), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para adicionar um acompanhamento a uma etapa
@produto_bp.route('/etapa/<int:etapa_id>/acompanhamento', methods=['POST'])
def adicionar_acompanhamento(etapa_id):
    try:
        acompanhamento_data = request.get_json()
        acompanhamento = adicionar_acompanhamento_a_etapa(etapa_id, acompanhamento_data)
        return jsonify(acompanhamento), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para remover uma etapa
@produto_bp.route('/etapa/<int:etapa_id>', methods=['DELETE'])
def remover_etapa(etapa_id):
    try:
        mensagem = remover_etapa(etapa_id)
        return jsonify(mensagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para remover um acompanhamento
@produto_bp.route('/acompanhamento/<int:acompanhamento_id>', methods=['DELETE'])
def remover_acompanhamento(acompanhamento_id):
    try:
        mensagem = remover_acompanhamento(acompanhamento_id)
        return jsonify(mensagem), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# # Rota para atualizar um produto com suas etapas e acompanhamentos
# @produto_bp.route('/produto/<int:produto_id>/completo', methods=['PUT'])
# def atualizar_completo(produto_id):
#     try:
#         produto_data = request.get_json()
#         produto = atualizar_produto_completo(produto_id, produto_data)
#         return jsonify(produto), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
