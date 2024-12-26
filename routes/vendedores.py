from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Vendedor
from schemas import VendedorSchema
from extensions import db

vendedor_bp = Blueprint('vendedor_bp', __name__)
vendedor_schema = VendedorSchema()
vendedores_schema = VendedorSchema(many=True)

@vendedor_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_vendedores():
    vendedores = Vendedor.query.all()
    return jsonify(vendedores_schema.dump(vendedores)), 200

@vendedor_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_vendedor(id):
    vendedor = Vendedor.query.get_or_404(id)
    return jsonify(vendedor_schema.dump(vendedor)), 200

@vendedor_bp.route('/', methods=['POST'])
@jwt_required()
def create_vendedor():
    data = request.get_json()
    errors = vendedor_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    vendedor = Vendedor(**data)
    db.session.add(vendedor)
    db.session.commit()
    return jsonify(vendedor_schema.dump(vendedor)), 201

@vendedor_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_vendedor(id):
    vendedor = Vendedor.query.get_or_404(id)
    data = request.get_json()
    errors = vendedor_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(vendedor, key, value)
    db.session.commit()
    return jsonify(vendedor_schema.dump(vendedor)), 200

@vendedor_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_vendedor(id):
    vendedor = Vendedor.query.get_or_404(id)
    db.session.delete(vendedor)
    db.session.commit()
    return jsonify({"message": "Vendedor eliminado exitosamente"}), 200
