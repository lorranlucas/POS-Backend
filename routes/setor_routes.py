from flask import Blueprint, request, jsonify
from services.setor_service import (
    obter_setores,
    cadastrar_setor,
    editar_setor,
    excluir_setor
)

setor_bp = Blueprint('setor_bp', __name__)

# Obter todos os setores
@setor_bp.route('/setor', methods=['GET'])
def get_setores():
    setores = obter_setores()
    return jsonify(setores)

# Cadastrar novo setor
@setor_bp.route('/setor', methods=['POST'])
def post_setor():
    data = request.get_json()
    nome_setor = data.get('nome')
    if not nome_setor:
        return jsonify({'message': 'Nome do setor é obrigatório!'}), 400
    setor = cadastrar_setor(nome_setor)
    if setor:
        return jsonify({'message': setor[0]['message']}), setor[1]
    return jsonify({'message': 'Erro ao cadastrar setor'}), 500

# Editar setor
@setor_bp.route('/setor/<int:id>', methods=['PUT'])
def put_setor(id):
    data = request.get_json()
    novo_nome = data.get('nome')
    if not novo_nome:
        return jsonify({'message': 'Novo nome do setor é obrigatório!'}), 400
    setor = editar_setor(id, novo_nome)
    return jsonify({'message': setor[0]['message']}), setor[1]

# Excluir setor
@setor_bp.route('/setor/<int:id>', methods=['DELETE'])
def delete_setor(id):
    setor = excluir_setor(id)
    return jsonify({'message': setor[0]['message']}), setor[1]
