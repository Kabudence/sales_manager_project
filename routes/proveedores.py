from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Proveedor
from schemas import ProveedorSchema
from extensions import db

proveedor_bp = Blueprint('proveedor_bp', __name__)
proveedor_schema = ProveedorSchema()
proveedores_schema = ProveedorSchema(many=True)


@proveedor_bp.route('/', methods=['GET'])
# @jwt_required()
def get_all_proveedores():
    """GET /api/proveedores/"""
    proveedores = Proveedor.query.all()
    return jsonify(proveedores_schema.dump(proveedores)), 200


@proveedor_bp.route('', methods=['POST'])
# @jwt_required()
def create_proveedor():
    """POST /api/proveedores/"""
    data = request.get_json()
    errors = proveedor_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Crea el proveedor
    nuevo = Proveedor(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(proveedor_schema.dump(nuevo)), 201


@proveedor_bp.route('/<int:id>', methods=['GET'])
# @jwt_required()
def get_proveedor(id):
    """GET /api/proveedores/<id>"""
    proveedor = Proveedor.query.get_or_404(id)
    return jsonify(proveedor_schema.dump(proveedor)), 200


@proveedor_bp.route('/<int:id>', methods=['PUT'])
# @jwt_required()
def update_proveedor(id):
    """PUT /api/proveedores/<id>"""
    proveedor = Proveedor.query.get_or_404(id)
    data = request.get_json()

    errors = proveedor_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Actualiza cada campo
    for key, value in data.items():
        setattr(proveedor, key, value)

    db.session.commit()
    return jsonify(proveedor_schema.dump(proveedor)), 200


@proveedor_bp.route('/<int:id>', methods=['DELETE'])
# @jwt_required()
def delete_proveedor(id):
    """DELETE /api/proveedores/<id>"""
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    return jsonify({"message": "Proveedor eliminado exitosamente"}), 200
