from decimal import Decimal
from sqlalchemy.orm import Session
from models.comandas.models_comadas import Comanda, ItemComanda, ItemComandaAcompanhamento, FormaPagamento
from models.cadastro.models_produto import Produto
from schemas.comanda.schemas_comanda import ComandaCreateSchema, ComandaSchema, ComandaUpdateSchema

class ComandaService:
    def __init__(self, db: Session):
        self.db = db

from decimal import Decimal
from sqlalchemy.orm import Session
from models.comandas.models_comadas import Comanda, ItemComanda, ItemComandaAcompanhamento, FormaPagamento
from models.cadastro.models_produto import Produto
from schemas.comanda.schemas_comanda import ComandaCreateSchema, ComandaSchema

class ComandaService:
    def __init__(self, db: Session):
        self.db = db

    def create_comanda(self, comanda_data: ComandaCreateSchema) -> Comanda:
        # Verificar se a mesa já tem uma comanda aberta
        if comanda_data.mesa_id:
            comanda_aberta = self.db.query(Comanda).filter(
                Comanda.mesa_id == comanda_data.mesa_id,
                Comanda.status == "aberta"
            ).first()
            if comanda_aberta:
                raise ValueError(f"A mesa {comanda_data.mesa_id} já possui uma comanda aberta (ID: {comanda_aberta.id})")

        ultima_comanda = self.db.query(Comanda).filter(Comanda.tipo == comanda_data.tipo).order_by(Comanda.id.desc()).first()
        if ultima_comanda and ultima_comanda.senha and ultima_comanda.senha.startswith("B"):
            ultimo_numero = int(ultima_comanda.senha[1:])
            nova_senha = f"B{(ultimo_numero + 1):03d}"
        else:
            nova_senha = "B001" if comanda_data.tipo == "balcao" else None

        valor_total = Decimal('0.00')
        nova_comanda = Comanda(
            tipo=comanda_data.tipo,
            mesa_id=comanda_data.mesa_id,
            senha=nova_senha,
            valor_total=valor_total,
            valor_pago=Decimal('0.00'),
            empresa_id=comanda_data.empresa_id,
            status="aberta"
        )
        self.db.add(nova_comanda)
        self.db.flush()

        for item_data in comanda_data.itens:
            produto = self.db.query(Produto).filter(Produto.id == item_data.produto_id).first()
            if not produto:
                raise ValueError(f"Produto {item_data.produto_id} não encontrado")
            
            preco_unitario = Decimal(produto.preco)
            item = ItemComanda(
                comanda_id=nova_comanda.id,
                produto_id=item_data.produto_id,
                quantidade=item_data.quantidade,
                preco_unitario=preco_unitario,
                empresa_id=comanda_data.empresa_id
            )
            self.db.add(item)
            self.db.flush()

            for acomp_data in item_data.acompanhamentos:
                acomp_produto = self.db.query(Produto).filter(Produto.id == acomp_data.produto_id).first()
                if not acomp_produto:
                    raise ValueError(f"Produto acompanhamento {acomp_data.produto_id} não encontrado")
                
                preco_adicional = Decimal(acomp_produto.preco) if acomp_produto.preco else Decimal('0.00')
                acompanhamento = ItemComandaAcompanhamento(
                    item_comanda_id=item.id,
                    produto_id=acomp_data.produto_id,
                    quantidade=acomp_data.quantidade,
                    preco_adicional=preco_adicional,
                    empresa_id=comanda_data.empresa_id
                )
                self.db.add(acompanhamento)
                valor_total += preco_adicional * acomp_data.quantidade

            valor_total += preco_unitario * item_data.quantidade

        nova_comanda.valor_total = valor_total
        self.db.commit()
        self.db.refresh(nova_comanda)
        return nova_comanda

    # Outros métodos permanecem iguais...


    def adicionar_forma_pagamento(self, comanda_id: int, metodo: str, valor_pago: Decimal) -> Comanda:
        comanda = self.db.query(Comanda).filter(Comanda.id == comanda_id).first()
        if not comanda:
            raise ValueError("Comanda não encontrada")

        # Adicionar nova forma de pagamento
        forma_pagamento = FormaPagamento(
            comanda_id=comanda_id,
            metodo=metodo,
            valor_pago=valor_pago,
            empresa_id=comanda.empresa_id
        )
        self.db.add(forma_pagamento)
        self.db.flush()

        # Atualizar o valor_pago da comanda
        comanda.valor_pago = (comanda.valor_pago or Decimal('0.00')) + valor_pago
        comanda.pago = comanda.valor_pago >= comanda.valor_total  # Campo booleano "pago" atualizado

        # Atualizar o status para "paga" se totalmente pago
        if comanda.pago and comanda.status != "paga":
            comanda.status = "paga"

        self.db.commit()
        self.db.refresh(comanda)
        return comanda

    def update_comanda_status(self, comanda_id: int, status: str) -> Comanda:
        comanda = self.db.query(Comanda).filter(Comanda.id == comanda_id).first()
        if not comanda:
            raise ValueError("Comanda não encontrada")

        comanda.status = status  # Atualiza apenas o status
        self.db.commit()
        self.db.refresh(comanda)
        return comanda

    def get_all_comandas(self):
        return self.db.query(Comanda).all()

    def get_comanda_by_id(self, comanda_id: int) -> Comanda:
        return self.db.query(Comanda).filter(Comanda.id == comanda_id).first()

    def update_comanda(self, comanda_id: int, comanda_data: ComandaUpdateSchema) -> Comanda:
        comanda = self.get_comanda_by_id(comanda_id)
        if not comanda:
            return None
        
        update_data = comanda_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(comanda, key, value)
        
        self.db.commit()
        self.db.refresh(comanda)
        return comanda

    def delete_comanda(self, comanda_id: int) -> bool:
        comanda = self.get_comanda_by_id(comanda_id)
        if not comanda:
            return False
        self.db.delete(comanda)
        self.db.commit()
        return True