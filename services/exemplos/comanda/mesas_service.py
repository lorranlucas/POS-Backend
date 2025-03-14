from app.extensions import db
from models.models_pedidos import Mesa

class MesaService:
    @staticmethod
    def criar_mesa(codg, posicao, status, type,area):
        nova_mesa = Mesa(codg=codg, posicao=posicao,status=status,type=type, area=area )
        db.session.add(nova_mesa)
        db.session.commit()
        return nova_mesa

    @staticmethod
    def obter_mesa_por_id(mesa_id):
        return Mesa.query.get(mesa_id)

    @staticmethod
    def atualizar_mesa(mesa_id, posicao_x=None, posicao_y=None):
        mesa = Mesa.query.get(mesa_id)
        if mesa:
            if posicao_x is not None:
                mesa.posicao_x = posicao_x
            if posicao_y is not None:
                mesa.posicao_y = posicao_y
            db.session.commit()
        return mesa

    @staticmethod
    def deletar_mesa(mesa_id):
        mesa = Mesa.query.get(mesa_id)
        if mesa:
            db.session.delete(mesa)
            db.session.commit()
            return True
        return False

    @staticmethod
    def listar_mesas():
        return Mesa.query.all()
