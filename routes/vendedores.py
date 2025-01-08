from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from models import Vendedor, Tienda
from schemas import VendedorSchema
from extensions import db

vendedor_bp = Blueprint('vendedor_bp', __name__)
vendedor_schema = VendedorSchema()
vendedores_schema = VendedorSchema(many=True)

# Obtener todos los vendedores
@vendedor_bp.route('/', methods=['GET'])
# @jwt_required()
def get_all_vendedores():
    vendedores = Vendedor.query.all()
    return jsonify(vendedores_schema.dump(vendedores)), 200

# Obtener un vendedor por ID
@vendedor_bp.route('/<int:idvend>', methods=['GET'])
# @jwt_required()
def get_vendedor(idvend):
    vendedor = Vendedor.query.get_or_404(idvend)
    return jsonify(vendedor_schema.dump(vendedor)), 200

# Crear un nuevo vendedor
@vendedor_bp.route('/', methods=['POST'])
def create_vendedor():
    try:
        data = request.get_json()
        schema = VendedorSchema()
        vendedor_data = schema.load(data)
        vendedor = Vendedor(**vendedor_data)
        db.session.add(vendedor)
        db.session.commit()
        return schema.dump(vendedor), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception as e:
        return {"error": str(e)}, 500


# Actualizar un vendedor existente
@vendedor_bp.route('/<int:idvend>', methods=['PUT'])
# @jwt_required()
def update_vendedor(idvend):
    vendedor = Vendedor.query.get_or_404(idvend)
    data = request.get_json()

    # Validar datos
    errors = vendedor_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Verificar si la nueva tienda existe
    if 'idemp' in data:
        tienda = Tienda.query.get(data['idemp'])
        if not tienda:
            return jsonify({"error": "La tienda especificada no existe"}), 404

    # Actualizar campos
    for key, value in data.items():
        setattr(vendedor, key, value)

    db.session.commit()
    return jsonify(vendedor_schema.dump(vendedor)), 200

# Eliminar un vendedor
@vendedor_bp.route('/<int:idvend>', methods=['DELETE'])
# @jwt_required()
def delete_vendedor(idvend):
    vendedor = Vendedor.query.get_or_404(idvend)
    db.session.delete(vendedor)
    db.session.commit()
    return jsonify({"message": "Vendedor eliminado exitosamente"}), 200
