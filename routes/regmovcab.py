from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import RegMovCab
from schemas import RegMovCabSchema
from extensions import db

regmovcab_bp = Blueprint('regmovcab_bp', __name__)
regmovcab_schema = RegMovCabSchema()
regmovcabs_schema = RegMovCabSchema(many=True)


# GET: Obtener todos los registros
@regmovcab_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_regmovcabs():
    regmovcabs = RegMovCab.query.all()
    return jsonify(regmovcabs_schema.dump(regmovcabs)), 200


# GET: Obtener un registro por ID
@regmovcab_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_regmovcab(id):
    regmovcab = RegMovCab.query.get_or_404(id)
    return jsonify(regmovcab_schema.dump(regmovcab)), 200


# POST: Crear un nuevo registro
@regmovcab_bp.route('/', methods=['POST'])
@jwt_required()
def create_regmovcab():
    data = request.get_json()

    # Validar datos de entrada
    errors = regmovcab_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Crear el nuevo registro
    regmovcab = RegMovCab(**data)
    db.session.add(regmovcab)
    db.session.commit()
    return jsonify(regmovcab_schema.dump(regmovcab)), 201


# PUT: Actualizar un registro existente
@regmovcab_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_regmovcab(id):
    regmovcab = RegMovCab.query.get_or_404(id)
    data = request.get_json()

    # Validar datos de entrada
    errors = regmovcab_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Actualizar los campos del registro
    for key, value in data.items():
        setattr(regmovcab, key, value)

    db.session.commit()
    return jsonify(regmovcab_schema.dump(regmovcab)), 200


# DELETE: Eliminar un registro
@regmovcab_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_regmovcab(id):
    regmovcab = RegMovCab.query.get_or_404(id)
    db.session.delete(regmovcab)
    db.session.commit()
    return jsonify({"message": "Registro eliminado exitosamente"}), 200


# GET: Obtener un registro por num_docum
@regmovcab_bp.route('/search/<string:num_docum>', methods=['GET'])
# @jwt_required()
def find_by_num_docum(num_docum):
    # Buscar el registro por num_docum
    regmovcab = RegMovCab.query.filter_by(num_docum=num_docum).first()

    if not regmovcab:
        return jsonify({"message": f"No se encontró un registro con num_docum: {num_docum}"}), 404

    return jsonify(regmovcab_schema.dump(regmovcab)), 200

@regmovcab_bp.route('/change-state-to-complete/<int:idmov>', methods=['PUT'])
# @jwt_required()
def change_state_to_complete(idmov):
    # Buscar el registro correspondiente por idmov
    regmovcab = RegMovCab.query.get(idmov)

    if not regmovcab:
        return jsonify({"message": f"No se encontró un registro con idmov: {idmov}"}), 404

    # Obtener los datos del body
    data = request.get_json()
    vendedor = data.get("vendedor")

    if not vendedor:
        return jsonify({"error": "El campo 'vendedor' es obligatorio"}), 400

    # Actualizar el estado y el vendedor
    regmovcab.estado = 1
    regmovcab.vendedor = vendedor
    db.session.commit()

    return jsonify({
        "message": f"Estado del registro con idmov {idmov} actualizado a '1' y vendedor modificado con éxito",
        "updated_record": regmovcab_schema.dump(regmovcab)
    }), 200
