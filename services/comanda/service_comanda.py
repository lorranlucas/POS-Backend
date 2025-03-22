from decimal import Decimal
from sqlalchemy.orm import Session
from models.comandas.models_comadas import Comanda, ItemComanda, ItemComandaAcompanhamento, FormaPagamento  # Corrigido "models_comadas" para "models_comandas"
from models.cadastro.models_produto import Produto
from schemas.comanda.schemas_comanda import ComandaCreateSchema, ComandaSchema, ComandaUpdateSchema

class ComandaService:
    def __init__(self, db: Session):
        self.db = db

    def create_comanda(self, comanda_data: ComandaCreateSchema) -> Comanda:
        """Cria uma nova comanda com itens e acompanhamentos."""
        # Verificar se a mesa já tem uma comanda aberta
        if comanda_data.mesa_id:
            comanda_aberta = self.db.query(Comanda).filter(
                Comanda.mesa_id == comanda_data.mesa_id,
                Comanda.status == "aberta"
            ).first()
            if comanda_aberta:
                raise ValueError(f"A mesa {comanda_data.mesa_id} já possui uma comanda aberta (ID: {comanda_aberta.id})")

        # Gerar senha para balcão
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
            
            preco_unitario = Decimal(str(produto.preco)) if produto.preco else Decimal('0.00')
            item = ItemComanda(
                comanda_id=nova_comanda.id,
                produto_id=item_data.produto_id,
                quantidade=item_data.quantidade,
                preco_unitario=preco_unitario,
                empresa_id=comanda_data.empresa_id,
                status_producao="pendente"  # Status inicial
            )
            self.db.add(item)
            self.db.flush()

            for acomp_data in item_data.acompanhamentos:
                acomp_produto = self.db.query(Produto).filter(Produto.id == acomp_data.produto_id).first()
                if not acomp_produto:
                    raise ValueError(f"Produto acompanhamento {acomp_data.produto_id} não encontrado")
                
                preco_adicional = Decimal(str(acomp_produto.preco)) if acomp_produto.preco else Decimal('0.00')
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

    def adicionar_forma_pagamento(self, comanda_id: int, metodo: str, valor_pago: Decimal) -> Comanda:
        """Adiciona uma forma de pagamento a uma comanda existente."""
        comanda = self.db.query(Comanda).filter(Comanda.id == comanda_id).first()
        if not comanda:
            raise ValueError("Comanda não encontrada")

        forma_pagamento = FormaPagamento(
            comanda_id=comanda_id,
            metodo=metodo,
            valor_pago=valor_pago,
            empresa_id=comanda.empresa_id
        )
        self.db.add(forma_pagamento)
        self.db.flush()

        comanda.valor_pago = (comanda.valor_pago or Decimal('0.00')) + valor_pago
        comanda.pago = comanda.valor_pago >= comanda.valor_total

        if comanda.pago and comanda.status != "paga":
            comanda.status = "paga"

        self.db.commit()
        self.db.refresh(comanda)
        return comanda

    def finalizar_comandas_mesa(self, mesa_id: int) -> bool:
        """Finaliza todas as comandas pagas de uma mesa."""
        comandas = self.db.query(Comanda).filter(Comanda.mesa_id == mesa_id).all()
        if not comandas:
            return False
        
        for comanda in comandas:
            if comanda.status != "paga":
                continue
            comanda.status = "fechada"
        
        self.db.commit()
        return True

    def update_comanda_status(self, comanda_id: int, status: str) -> Comanda:
        """Atualiza o status de uma comanda."""
        comanda = self.db.query(Comanda).filter(Comanda.id == comanda_id).first()
        if not comanda:
            raise ValueError("Comanda não encontrada")

        comanda.status = status
        self.db.commit()
        self.db.refresh(comanda)
        return comanda

    def get_itens_by_status_producao(self, status_producao: str, empresa_id: int) -> list[ItemComanda]:
        """Busca itens de comandas por status de produção para uma empresa específica."""
        return self.db.query(ItemComanda).join(Comanda).join(Produto, ItemComanda.produto_id == Produto.id).filter(
            ItemComanda.status_producao == status_producao,
            Comanda.empresa_id == empresa_id,
            Comanda.status.in_(["aberta", "paga"])
        ).all()

    def update_item_status_producao(self, item_id: int, status_producao: str) -> ItemComanda:
        """Atualiza o status de produção de um item específico."""
        item = self.db.query(ItemComanda).filter(ItemComanda.id == item_id).first()
        if not item:
            raise ValueError("Item não encontrado")
        if status_producao not in ["pendente", "em produção", "pronto", "entregue"]:
            raise ValueError("Status de produção inválido")
        
        item.status_producao = status_producao
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_all_comandas(self) -> list[Comanda]:
        """Retorna todas as comandas."""
        return self.db.query(Comanda).all()

    def get_comanda_by_id(self, comanda_id: int) -> Comanda:
        """Retorna uma comanda específica pelo ID."""
        comanda = self.db.query(Comanda).filter(Comanda.id == comanda_id).first()
        return comanda

    def update_comanda(self, comanda_id: int, comanda_data: ComandaUpdateSchema) -> Comanda:
        """Atualiza os dados de uma comanda."""
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
        """Deleta uma comanda pelo ID."""
        comanda = self.get_comanda_by_id(comanda_id)
        if not comanda:
            return False
        self.db.delete(comanda)
        self.db.commit()
        return True