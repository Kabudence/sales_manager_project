from flask import Blueprint, request, jsonify
from models import Cliente
from schemas import ClienteSchema
from extensions import db

cliente_bp = Blueprint('cliente_bp', __name__)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

# Ojo: usaremos route('') en lugar de route('/')
@cliente_bp.route('/', methods=['GET'])
# @jwt_required()
def get_all_clientes():
    clientes = Cliente.query.all()
    return jsonify(clientes_schema.dump(clientes)), 200

@cliente_bp.route('', methods=['POST'])
def create_cliente():
    data = request.get_json()
    errors = cliente_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    cliente = Cliente(**data)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente_schema.dump(cliente)), 201

@cliente_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente_schema.dump(cliente)), 200

@cliente_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()
    errors = cliente_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(cliente, key, value)
    db.session.commit()
    return jsonify(cliente_schema.dump(cliente)), 200

@cliente_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado exitosamente"}), 200
