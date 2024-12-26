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

@clase_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_clase(id):
    clase = Clase.query.get_or_404(id)
    return jsonify(clase_schema.dump(clase)), 200

@clase_bp.route('/', methods=['POST'])
@jwt_required()
def create_clase():
    data = request.get_json()
    errors = clase_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    clase = Clase(**data)
    db.session.add(clase)
    db.session.commit()
    return jsonify(clase_schema.dump(clase)), 201

@clase_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_clase(id):
    clase = Clase.query.get_or_404(id)
    data = request.get_json()
    errors = clase_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(clase, key, value)
    db.session.commit()
    return jsonify(clase_schema.dump(clase)), 200

@clase_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_clase(id):
    clase = Clase.query.get_or_404(id)
    db.session.delete(clase)
    db.session.commit()
    return jsonify({"message": "Clase eliminada exitosamente"}), 200
