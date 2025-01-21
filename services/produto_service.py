from extensions import db
from models import Produto, Etapa, EtapaAcompanhamento

def criar_produto(produto_data):
    # Garantir que 'tipo' está presente
    tipo = produto_data.get('tipo')
    if not tipo:
        raise ValueError("O campo 'tipo' é obrigatório.")

    # Criar novo produto
    novo_produto = Produto(
        nome=produto_data['nome'],
        descricao=produto_data.get('descricao'),
        tipo=tipo,
        codigo_de_barra=produto_data.get('codigo_de_barra'),
        disponibilidade=produto_data['disponibilidade'],
        preco=produto_data.get('preco'),
        id_und_med=produto_data.get('id_und_med'),
        foto=produto_data.get('foto')
    )

    # Adicionar o produto à sessão
    db.session.add(novo_produto)

    # Se for tipo 'combo' e existir 'etapas', adicionar as etapas
    if tipo == 'combo' and 'etapas' in produto_data:
        for etapa_data in produto_data['etapas']:
            # Criar a etapa
            etapa = Etapa(produto_id=novo_produto.id, nome=etapa_data['nome'], posicao=etapa_data['posicao'])
            db.session.add(etapa)

            # Verificar e adicionar acompanhamentos, se existirem
            if 'acompanhamentos' in etapa_data and isinstance(etapa_data['acompanhamentos'], list):
                for acompanhamento_data in etapa_data['acompanhamentos']:
                    acompanhamento = EtapaAcompanhamento(
                        id_etapa=etapa.id,
                        id_produto=acompanhamento_data['id_produto'],
                        preco=acompanhamento_data.get('preco')  # Preço opcional
                    )
                    db.session.add(acompanhamento)

    # Commit único após todas as inserções
    db.session.commit()

    # Retornar o produto criado
    return novo_produto.to_dict()

def listar_produtos():
    try:
        produtos = Produto.query.all()
        return [produto.to_dict() for produto in produtos]
    except Exception as e:
        raise Exception(f"Erro ao listar produtos: {str(e)}")

def atualizar_produto(produto_id, produto_data):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")
        
        produto.nome = produto_data.get('nome', produto.nome)
        produto.descricao = produto_data.get('descricao', produto.descricao)
        produto.tipo = produto_data.get('tipo', produto.tipo)
        produto.codigo_de_barra = produto_data.get('codigo_de_barra', produto.codigo_de_barra)
        produto.disponibilidade = produto_data.get('disponibilidade', produto.disponibilidade)
        produto.preco = produto_data.get('preco', produto.preco)
        produto.id_und_med = produto_data.get('id_und_med', produto.id_und_med)
        produto.foto = produto_data.get('foto', produto.foto)
        
        db.session.commit()
        return produto.to_dict()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar produto: {str(e)}")

def remover_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")
        
        db.session.delete(produto)
        db.session.commit()
        return {"message": "Produto removido com sucesso."}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao remover produto: {str(e)}")

def listar_produtos_com_etapas_e_acompanhamentos():
    try:
        produtos = Produto.query.all()
        resultado = []
        for produto in produtos:
            produto_dict = produto.to_dict()
            produto_dict['etapas'] = [etapa.to_dict() for etapa in produto.etapas]
            for etapa in produto.etapas:
                etapa_dicts = [acompanhamento.to_dict() for acompanhamento in etapa.acompanhamentos]
                produto_dict['etapas_acompanhamentos'] = etapa_dicts
            resultado.append(produto_dict)
        return resultado
    except Exception as e:
        raise Exception(f"Erro ao listar produtos com etapas e acompanhamentos: {str(e)}")

def adicionar_etapa_a_produto(produto_id, etapa_data):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")

        nova_etapa = Etapa(produto_id=produto_id, nome=etapa_data['nome'], posicao=etapa_data['posicao'])
        db.session.add(nova_etapa)
        db.session.commit()
        return nova_etapa.to_dict()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao adicionar etapa ao produto: {str(e)}")

def adicionar_acompanhamento_a_etapa(etapa_id, acompanhamento_data):
    try:
        etapa = Etapa.query.get(etapa_id)
        if not etapa:
            raise Exception("Etapa não encontrada.")
        
        novo_acompanhamento = EtapaAcompanhamento(
            id_etapa=etapa_id,
            id_produto=acompanhamento_data['id_produto'],
            preco=acompanhamento_data.get('preco')
        )
        db.session.add(novo_acompanhamento)
        db.session.commit()
        return novo_acompanhamento.to_dict()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao adicionar acompanhamento à etapa: {str(e)}")

def remover_etapa(etapa_id):
    try:
        etapa = Etapa.query.get(etapa_id)
        if not etapa:
            raise Exception("Etapa não encontrada.")
        
        db.session.delete(etapa)
        db.session.commit()
        return {"message": "Etapa removida com sucesso."}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao remover etapa: {str(e)}")

def remover_acompanhamento(acompanhamento_id):
    try:
        acompanhamento = EtapaAcompanhamento.query.get(acompanhamento_id)
        if not acompanhamento:
            raise Exception("Acompanhamento não encontrado.")
        
        db.session.delete(acompanhamento)
        db.session.commit()
        return {"message": "Acompanhamento removido com sucesso."}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao remover acompanhamento: {str(e)}")

def atualizar_produto_completo(produto_id, produto_data):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            raise Exception("Produto não encontrado.")
        
        # Atualizar o produto
        produto.nome = produto_data.get('nome', produto.nome)
        produto.descricao = produto_data.get('descricao', produto.descricao)
        produto.tipo = produto_data.get('tipo', produto.tipo)
        produto.codigo_de_barra = produto_data.get('codigo_de_barra', produto.codigo_de_barra)
        produto.disponibilidade = produto_data.get('disponibilidade', produto.disponibilidade)
        produto.preco = produto_data.get('preco', produto.preco)
        produto.id_und_med = produto_data.get('id_und_med', produto.id_und_med)
        produto.foto = produto_data.get('foto', produto.foto)

        # Atualizar etapas se necessário
        if 'etapas' in produto_data:
            for etapa_data in produto_data['etapas']:
                etapa = Etapa.query.filter_by(produto_id=produto_id, id=etapa_data['id']).first()
                if etapa:
                    # Atualizar a etapa existente
                    etapa.nome = etapa_data.get('nome', etapa.nome)
                    etapa.posicao = etapa_data.get('posicao', etapa.posicao)
                else:
                    # Criar nova etapa se não existir
                    nova_etapa = Etapa(
                        produto_id=produto_id, 
                        nome=etapa_data['nome'], 
                        posicao=etapa_data['posicao']
                    )
                    db.session.add(nova_etapa)
                    db.session.commit()

                # Atualizar acompanhamentos das etapas
                if 'acompanhamentos' in etapa_data:
                    for acompanhamento_data in etapa_data['acompanhamentos']:
                        acompanhamento = EtapaAcompanhamento.query.filter_by(
                            id_etapa=etapa.id, id_produto=acompanhamento_data['id_produto']
                        ).first()
                        if acompanhamento:
                            # Atualizar acompanhamento existente
                            acompanhamento.preco = acompanhamento_data.get('preco', acompanhamento.preco)
                        else:
                            # Adicionar novo acompanhamento
                            novo_acompanhamento = EtapaAcompanhamento(
                                id_etapa=etapa.id,
                                id_produto=acompanhamento_data['id_produto'],
                                preco=acompanhamento_data.get('preco')
                            )
                            db.session.add(novo_acompanhamento)

        db.session.commit()
        return produto.to_dict()

    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar produto completo: {str(e)}")

