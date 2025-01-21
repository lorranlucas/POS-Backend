from models import Setor
from extensions import db
import logging

logging.basicConfig(level=logging.DEBUG)  # Configura o logging

def cadastrar_setor(setor_nome):
    try:
        logging.debug(f"Cadastrando setor: {setor_nome}")  # Log para ver o nome do setor
        novo_setor = Setor(nome=setor_nome)
        db.session.add(novo_setor)
        db.session.commit()
        return {"message": "Setor cadastrado com sucesso!"}, 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao cadastrar setor: {str(e)}")  # Log de erro
        return {"message": f"Erro ao cadastrar setor: {str(e)}"}, 500


# Função para obter todos os setores
def obter_setores():
    try:
        # Obtendo todos os setores do banco de dados
        setores = Setor.query.all()

        # Retornando os setores como lista de dicionários
        return [setor.to_dict() for setor in setores]
    except Exception as e:
        return {"message": f"Erro ao obter setores: {str(e)}"}, 500

# Função para editar um setor existente
def editar_setor(setor_id, novo_nome):
    try:
        # Encontrando o setor pelo ID
        setor = Setor.query.get(setor_id)

        if setor:
            # Atualizando o nome do setor
            setor.nome = novo_nome
            db.session.commit()
            return {"message": f"Setor {setor_id} atualizado com sucesso!"}, 200
        else:
            return {"message": "Setor não encontrado!"}, 404
    except Exception as e:
        db.session.rollback()
        return {"message": f"Erro ao editar setor: {str(e)}"}, 500

# Função para excluir um setor
def excluir_setor(setor_id):
    try:
        # Encontrando o setor pelo ID
        setor = Setor.query.get(setor_id)

        if setor:
            # Excluindo o setor
            db.session.delete(setor)
            db.session.commit()
            return {"message": f"Setor {setor_id} excluído com sucesso!"}, 200
        else:
            return {"message": "Setor não encontrado!"}, 404
    except Exception as e:
        db.session.rollback()
        return {"message": f"Erro ao excluir setor: {str(e)}"}, 500
