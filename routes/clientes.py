from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Cliente
from schemas import ClienteSchema
from extensions import db

cliente_bp = Blueprint('cliente_bp', __name__)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)


@cliente_bp.route('', methods=['GET'])
@jwt_required()
def get_all_clientes():

    clientes = Cliente.query.all()
    return jsonify(clientes_schema.dump(clientes)), 200


@cliente_bp.route('', methods=['POST'])
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

@cliente_bp.route('/<int:id>', methods=['GET'])

def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente_schema.dump(cliente)), 200

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
@jwt_required()
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado exitosamente"}), 200


@cliente_bp.route('/automatic-create', methods=['POST'])
def automatic_create_cliente():
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        party_client = data.get("PartyClient")

        # Validar que los datos necesarios existan
        if not party_client:
            return jsonify({"error": "Faltan los datos en 'PartyClient'"}), 400

        identify_code = party_client.get("IdentifyCode")
        registration_name = party_client.get("RegistrationName")

        if not identify_code or not registration_name:
            return jsonify({"error": "Faltan datos obligatorios: IdentifyCode o RegistrationName"}), 400

        # Generar valores para los campos del cliente
        idcliente = identify_code  # `idcliente` se genera automáticamente como `IdentifyCode`
        tdoc = "D" if len(identify_code) == 8 and identify_code.isdigit() else "R"
        nomcliente = registration_name
        direccion = "TRUJILLO"  # Automático
        telefono = "111111"  # Automático
        estado = 1  # Estado predeterminado

        # Verificar si el cliente ya existe
        cliente_existente = Cliente.query.get(idcliente)
        if cliente_existente:
            # Si el cliente ya existe, devolver una respuesta como si fuera una creación exitosa
            return jsonify({
                "message": "El cliente ya existe, devolviendo datos existentes.",
                "cliente": cliente_schema.dump(cliente_existente)
            }), 200

        # Crear el nuevo cliente
        nuevo_cliente = Cliente(
            idcliente=idcliente,
            tdoc=tdoc,
            nomcliente=nomcliente,
            direccion=direccion,
            telefono=telefono,
            estado=estado
        )

        # Guardar el cliente en la base de datos
        db.session.add(nuevo_cliente)
        db.session.commit()

        return jsonify({
            "message": "Cliente creado automáticamente con éxito",
            "cliente": cliente_schema.dump(nuevo_cliente)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


