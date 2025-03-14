from flask import Blueprint, jsonify, request
from models.models_config import Impressora, db
import platform
import subprocess

printer_bp = Blueprint("printer", __name__)

def get_system_printers():
    system = platform.system()
    printers = []

    if system == "Windows":
        try:
            import win32print
            printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        except Exception as e:
            return {"error": f"Erro ao buscar impressoras no Windows: {e}"}

    else:  # Linux e macOS
        try:
            result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
            lines = result.stdout.split("\n")
            for line in lines:
                if "printer" in line:
                    printers.append(line.split()[1])  # Extrai o nome da impressora
        except Exception as e:
            return {"error": f"Erro ao buscar impressoras no sistema: {e}"}

    return {"printers": printers}

@printer_bp.route("/printers", methods=["GET"])
def list_printers():
    return jsonify(get_system_printers())

@printer_bp.route("/printers/cadastradas", methods=["GET"])
def list_registered_printers():
    printers = Impressora.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "setor": p.setor, "tipo": p.tipo} for p in printers])

@printer_bp.route("/printers", methods=["POST"])
def add_printer():
    data = request.json
    nova_impressora = Impressora(nome=data["nome"], setor=data["setor"], tipo=data["tipo"])
    db.session.add(nova_impressora)
    db.session.commit()
    return jsonify({"message": "Impressora cadastrada com sucesso!"}), 201
