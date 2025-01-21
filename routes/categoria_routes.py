from flask import Blueprint, request, jsonify
from services.categoria_service import (
    listar_categorias, 
    criar_categoria, 
    atualizar_categoria, 
    remover_categoria
)

categoria_bp = Blueprint('categoria_bp', __name__)

# Listar todas as categorias com paginação e filtro
@categoria_bp.route('/categorias', methods=['GET'])
def listar():
    try:
        pagina = int(request.args.get('pagina', 1))  # Página atual
        itens_por_pagina = int(request.args.get('itens_por_pagina', 10))  # Itens por página
        filtro = request.args.get('filtro', '')  # Texto para filtrar categorias

        categorias, total, paginas = listar_categorias(pagina, itens_por_pagina, filtro)
        return jsonify({
            "dados": categorias,
            "total": total,
            "paginas": paginas,
            "pagina_atual": pagina,
            "itens_por_pagina": itens_por_pagina
        }), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar categorias: {str(e)}'}), 500

# Criar nova categoria
@categoria_bp.route('/categorias', methods=['POST'])
def criar():
    try:
        dados = request.get_json()
        nome_categoria = dados.get('nome')
        if not nome_categoria:
            return jsonify({'mensagem': 'O nome da categoria é obrigatório!'}), 400
        criar_categoria(nome_categoria)
        return jsonify({'mensagem': 'Categoria criada com sucesso!'}), 201
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar categoria: {str(e)}'}), 500

# Atualizar categoria
@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
def atualizar(id):
    try:
        dados = request.get_json()
        novo_nome = dados.get('nome')
        if not novo_nome:
            return jsonify({'mensagem': 'O novo nome da categoria é obrigatório!'}), 400
        atualizar_categoria(id, novo_nome)
        return jsonify({'mensagem': 'Categoria atualizada com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar categoria: {str(e)}'}), 500

# Remover categoria
@categoria_bp.route('/categorias/<int:id>', methods=['DELETE'])
def remover(id):
    try:
        remover_categoria(id)
        return jsonify({'mensagem': 'Categoria removida com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao remover categoria: {str(e)}'}), 500
