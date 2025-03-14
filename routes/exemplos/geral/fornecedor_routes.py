from flask import Blueprint, request, jsonify
from services.geral.fornecedor_service import (
    listar_fornecedores,
    criar_fornecedor,
    atualizar_fornecedor,
    remover_fornecedor
)

fornecedor_bp = Blueprint('fornecedor_bp', __name__)

# Listar todos os fornecedores com paginação e filtro
@fornecedor_bp.route('/fornecedores', methods=['GET'])
def listar():
    try:
        pagina = int(request.args.get('pagina', 1))
        itens_por_pagina = int(request.args.get('itens_por_pagina', 10))
        filtro = request.args.get('filtro', '')

        fornecedores, total, paginas = listar_fornecedores(pagina, itens_por_pagina, filtro)
        return jsonify({
            "dados": fornecedores,
            "total": total,
            "paginas": paginas,
            "pagina_atual": pagina,
            "itens_por_pagina": itens_por_pagina
        }), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar fornecedores: {str(e)}'}), 500

# Criar um novo fornecedor
@fornecedor_bp.route('/fornecedores', methods=['POST'])
def criar():
    try:
        dados = request.get_json()
        codigo = dados.get('codigo')
        nome = dados.get('nome')
        email = dados.get('email')

        if not codigo or not nome or not email:
            return jsonify({'mensagem': 'Código, nome e email são obrigatórios!'}), 400

        criar_fornecedor(codigo, nome, email)
        return jsonify({'mensagem': 'Fornecedor criado com sucesso!'}), 201
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar fornecedor: {str(e)}'}), 500

# Atualizar um fornecedor
@fornecedor_bp.route('/fornecedores/<int:id>', methods=['PUT'])
def atualizar(id):
    try:
        dados = request.get_json()
        codigo = dados.get('codigo')
        nome = dados.get('nome')
        email = dados.get('email')

        if not codigo or not nome or not email:
            return jsonify({'mensagem': 'Código, nome e email são obrigatórios!'}), 400

        atualizar_fornecedor(id, codigo, nome, email)
        return jsonify({'mensagem': 'Fornecedor atualizado com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar fornecedor: {str(e)}'}), 500

# Remover um fornecedor
@fornecedor_bp.route('/fornecedores/<int:id>', methods=['DELETE'])
def remover(id):
    try:
        remover_fornecedor(id)
        return jsonify({'mensagem': 'Fornecedor removido com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao remover fornecedor: {str(e)}'}), 500
