from flask import Blueprint, request, jsonify
from models import Compra
from schemas import CompraSchema
from extensions import db

compra_bp = Blueprint('compra_bp', __name__)

compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)

# Obtener todas las compras
@compra_bp.route('/', methods=['GET'])
def get_all_compras():
    compras = Compra.query.all()
    return jsonify(compras_schema.dump(compras)), 200

# Crear una nueva compra
@compra_bp.route('/', methods=['POST'])
def create_compra():
    data = request.get_json()
    errors = compra_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    nueva_compra = Compra(**data)
    db.session.add(nueva_compra)
    db.session.commit()

    return jsonify(compra_schema.dump(nueva_compra)), 201

# Obtener una compra por ID
@compra_bp.route('/<int:id>', methods=['GET'])
def get_compra(id):
    compra = Compra.query.get_or_404(id)
    return jsonify(compra_schema.dump(compra)), 200

# Actualizar una compra
@compra_bp.route('/<int:id>', methods=['PUT'])
def update_compra(id):
    compra = Compra.query.get_or_404(id)
    data = request.get_json()
    errors = compra_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(compra, key, value)

    db.session.commit()
    return jsonify(compra_schema.dump(compra)), 200

# Eliminar una compra
@compra_bp.route('/<int:id>', methods=['DELETE'])
def delete_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()

    return jsonify({"message": "Compra eliminada exitosamente"}), 200
