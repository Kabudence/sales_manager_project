from flask import Blueprint, request, jsonify
from models import Cliente
from schemas import ClienteSchema
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

cliente_bp = Blueprint('cliente_bp', __name__)
cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)




@cliente_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_clientes():
    current_user = get_jwt_identity()  # Asegúrate de que sea una cadena
    print(f"Usuario autenticado: {current_user}")  # Debug
    clientes = Cliente.query.all()
    return jsonify(clientes_schema.dump(clientes)), 200

@cliente_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente_schema.dump(cliente)), 200


@cliente_bp.route('/', methods=['POST'])
@jwt_required()
def create_cliente():
    data = request.get_json()
    errors = cliente_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    cliente = Cliente(**data)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente_schema.dump(cliente)), 201


@cliente_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
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
