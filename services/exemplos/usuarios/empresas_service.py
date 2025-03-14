from app.extensions import db
from models.models_user import Empresa, Licenca
from datetime import datetime, timedelta
import uuid

class EmpresaService:
    @staticmethod
    def cadastrar_empresa(nome, cnpj_cpf, email_contato, senha, tipo_licenca='free', valor=0.0, subpacotes=None):
        """Cria uma nova empresa e registra no banco de dados"""
        try:
            # Criar a empresa
            nova_empresa = Empresa(nome=nome, cnpj_cpf=cnpj_cpf, email_contato=email_contato, senha=senha)
            
            # Criar licença inicial
            nova_licenca = Licenca(
                tipo=tipo_licenca,
                valor=valor,
                subpacotes=subpacotes or {},
                data_expiracao=datetime.utcnow() + timedelta(days=7) if tipo_licenca == 'free' else datetime.utcnow() + timedelta(days=30),
                codigo_licenca=str(uuid.uuid4())
            )

            nova_empresa.licenca = nova_licenca

            # Salvar no banco
            db.session.add(nova_empresa)
            db.session.commit()

            return {"mensagem": "Empresa cadastrada com sucesso!", "empresa_id": nova_empresa.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"erro": str(e)}, 500
