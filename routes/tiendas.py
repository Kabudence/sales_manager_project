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
    return jsonify([{"idemp": tienda.idemp, "nombree": tienda.nombree} for tienda in tiendas]), 200

# Crear una nueva tienda
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

# Actualizar una tienda existente
@tienda_bp.route('/<string:idemp>', methods=['PUT'])
@jwt_required()
def update_tienda(idemp):
    tienda = Tienda.query.get_or_404(idemp)
    data = request.get_json()
    errors = tienda_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(tienda, key, value)

    db.session.commit()
    return jsonify(tienda_schema.dump(tienda)), 200

# Eliminar una tienda
@tienda_bp.route('/<string:idemp>', methods=['DELETE'])
@jwt_required()
def delete_tienda(idemp):
    tienda = Tienda.query.get_or_404(idemp)
    db.session.delete(tienda)
    db.session.commit()
    return jsonify({"message": "Tienda eliminada exitosamente"}), 200
