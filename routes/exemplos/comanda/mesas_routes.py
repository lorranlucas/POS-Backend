

from flask import Blueprint, request, jsonify
from services.comanda import (
    balcao_service, 
    comanda_service, 
    mesas_service
)

MesaService = mesas_service.MesaService()

mesa_bp = Blueprint("mesa_bp", __name__)

@mesa_bp.route("/mesas", methods=["GET"])
def listar_mesas():
    print('listar_mesas')
    mesas = MesaService.listar_mesas()
    return jsonify([mesa.to_dict() for mesa in mesas])

@mesa_bp.route("/mesas", methods=["POST"])
def criar_mesa():
    print('criar_mesa')
    data = request.json
    print(data)
    nova_mesa = MesaService.criar_mesa(
        codg=data["mesaId"], 
        posicao=data["posicao"],
        status=data["status"], 
        type=data["type"],
        area=data["area"]
    )   
    return jsonify(nova_mesa.to_dict()), 201

@mesa_bp.route("/mesas/<int:mesa_id>", methods=["PUT"])
def atualizar_mesa(mesa_id):
    print('atualizar_mesa')
    data = request.json
    mesa_atualizada = MesaService.atualizar_mesa(
        mesa_id, posicao_x=data.get("posicao_x"), posicao_y=data.get("posicao_y")
    )
    return jsonify(mesa_atualizada.to_dict()) if mesa_atualizada else ("", 404)
