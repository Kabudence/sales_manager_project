from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Producto, Linea
from schemas import ProductoSchema
from extensions import db

producto_bp = Blueprint('producto_bp', __name__)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@producto_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_productos():
    productos = Producto.query.all()
    return jsonify(productos_schema.dump(productos)), 200

@producto_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def get_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(producto_schema.dump(producto)), 200

@producto_bp.route('/', methods=['POST'])
@jwt_required()
def create_producto():
    data = request.get_json()

    # Validar datos de entrada con el esquema
    errors = producto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Verificar si la línea (FK) existe
    linea_id = data.get('linea_id')
    linea = Linea.query.get(linea_id)
    if not linea:
        return jsonify({"error": "La línea especificada no existe"}), 404

    # Crear el producto si la línea es válida
    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto_schema.dump(producto)), 201

@producto_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
def update_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()

    # Validar datos de entrada
    errors = producto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Verificar si la nueva línea (FK) existe
    linea_id = data.get('linea_id')
    if linea_id:
        linea = Linea.query.get(linea_id)
        if not linea:
            return jsonify({"error": "La línea especificada no existe"}), 404

    # Actualizar los campos del producto
    for key, value in data.items():
        setattr(producto, key, value)

    db.session.commit()
    return jsonify(producto_schema.dump(producto)), 200
