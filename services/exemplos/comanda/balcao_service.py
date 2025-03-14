from app.extensions import db
from models.models_pedidos import Balcao

class BalcaoService:
    @staticmethod
    def criar_balcao(codg):
        novo_balcao = Balcao(codg=codg)
        db.session.add(novo_balcao)
        db.session.commit()
        return novo_balcao

    @staticmethod
    def obter_balcao_por_id(balcao_id):
        return Balcao.query.get(balcao_id)

    @staticmethod
    def deletar_balcao(balcao_id):
        balcao = Balcao.query.get(balcao_id)
        if balcao:
            db.session.delete(balcao)
            db.session.commit()
            return True
        return False

    @staticmethod
    def listar_balcoes():
        return Balcao.query.all()
