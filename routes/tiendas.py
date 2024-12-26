from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Tienda
from schemas import TiendaSchema
from extensions import db

tienda_bp = Blueprint('tienda_bp', __name__)
tienda_schema = TiendaSchema()
tiendas_schema = TiendaSchema(many=True)

@tienda_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_tiendas():
    tiendas = Tienda.query.all()
    return jsonify(tiendas_schema.dump(tiendas)), 200

@tienda_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_tienda(id):
    tienda = Tienda.query.get_or_404(id)
    return jsonify(tienda_schema.dump(tienda)), 200

@tienda_bp.route('/', methods=['POST'])
@jwt_required()
def create_tienda():
    data = request.get_json()
    errors = tienda_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tienda = Tienda(**data)
    db.session.add(tienda)
    db.session.commit()
    return jsonify(tienda_schema.dump(tienda)), 201

@tienda_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_tienda(id):
    tienda = Tienda.query.get_or_404(id)
    data = request.get_json()
    errors = tienda_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(tienda, key, value)
    db.session.commit()
    return jsonify(tienda_schema.dump(tienda)), 200

@tienda_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tienda(id):
    tienda = Tienda.query.get_or_404(id)
    db.session.delete(tienda)
    db.session.commit()
    return jsonify({"message": "Tienda eliminada exitosamente"}), 200
