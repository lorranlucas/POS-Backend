from app.extensions import db
from models.models_pedidos import Comanda

class ComandaService:
    @staticmethod
    def criar_comanda(codg, mesa_id=None, balcao_id=None):
        nova_comanda = Comanda(codg=codg, mesa_id=mesa_id, balcao_id=balcao_id)
        db.session.add(nova_comanda)
        db.session.commit()
        return nova_comanda

    @staticmethod
    def obter_comanda_por_id(comanda_id):
        return Comanda.query.get(comanda_id)

    @staticmethod
    def atualizar_comanda(comanda_id, status=None, total=None):
        comanda = Comanda.query.get(comanda_id)
        if comanda:
            if status is not None:
                comanda.status = status
            if total is not None:
                comanda.total = total
            db.session.commit()
        return comanda

    @staticmethod
    def deletar_comanda(comanda_id):
        comanda = Comanda.query.get(comanda_id)
        if comanda:
            db.session.delete(comanda)
            db.session.commit()
            return True
        return False

    @staticmethod
    def listar_comandas():
        return Comanda.query.all()
