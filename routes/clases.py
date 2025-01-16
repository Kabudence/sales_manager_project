from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Clase
from schemas import ClaseSchema
from extensions import db

clase_bp = Blueprint('clase_bp', __name__)
clase_schema = ClaseSchema()
clases_schema = ClaseSchema(many=True)

@clase_bp.route('/', methods=['GET'])
@jwt_required()

def get_all_clases():
    clases = Clase.query.all()
    return jsonify(clases_schema.dump(clases)), 200


@clase_bp.route('', methods=['POST'])
@jwt_required()

def create_clase():
    data = request.get_json()
    errors = clase_schema.validate(data)  # Validar datos de entrada
    if errors:
        return jsonify(errors), 400

    nueva_clase = Clase(
        nombres=data["nombres"],
        idemp=data["idemp"],
        estado=data["estado"]
    )
    db.session.add(nueva_clase)
    db.session.commit()

    return jsonify(clase_schema.dump(nueva_clase)), 201
@clase_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_clase(id):
    clase = Clase.query.get_or_404(id)
    return jsonify(clase_schema.dump(clase)), 200


@clase_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_clase(id):
    clase = Clase.query.get_or_404(id)
    data = request.get_json()

    # Actualizar campos
    if "nombres" in data:
        clase.nombres = data["nombres"]
    if "idemp" in data:
        clase.idemp = data["idemp"]
    if "estado" in data:
        clase.estado = data["estado"]

    db.session.commit()

    return jsonify({"message": "Clase actualizada con éxito"}), 200

@clase_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_clase(id):
    clase = Clase.query.get_or_404(id)
    db.session.delete(clase)
    db.session.commit()

    return jsonify({"message": "Clase eliminada con éxito"}), 200
