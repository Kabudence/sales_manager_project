from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import RegMovDet
from schemas import RegMovDetSchema

# Crear el Blueprint para regmovdet
regmovdet_bp = Blueprint('regmovdet_bp', __name__)

# Crear los esquemas para serialización
regmovdet_schema = RegMovDetSchema()
regmovdets_schema = RegMovDetSchema(many=True)

# GET: Obtener todos los registros
@regmovdet_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_regmovdet():
    regmovdets = RegMovDet.query.all()
    return jsonify(regmovdets_schema.dump(regmovdets)), 200


# GET: Obtener un registro por iddet
@regmovdet_bp.route('/<int:iddet>', methods=['GET'])
@jwt_required()
def get_regmovdet(iddet):
    regmovdet = RegMovDet.query.get_or_404(iddet)
    return jsonify(regmovdet_schema.dump(regmovdet)), 200


# GET: Obtener registros por idcab
@regmovdet_bp.route('/by-idcab/<int:idcab>', methods=['GET'])
# @jwt_required()
def get_regmovdet_by_idcab(idcab):
    regmovdets = RegMovDet.query.filter_by(idcab=idcab).all()
    if not regmovdets:
        return jsonify({"message": f"No se encontraron registros para idcab {idcab}"}), 404
    return jsonify(regmovdets_schema.dump(regmovdets)), 200


# POST: Crear un nuevo registro
@regmovdet_bp.route('/', methods=['POST'])
# @jwt_required()
def create_regmovdet():
    data = request.get_json()

    # Validar los datos de entrada
    errors = regmovdet_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Crear el nuevo registro
    regmovdet = RegMovDet(**data)
    db.session.add(regmovdet)
    db.session.commit()
    return jsonify(regmovdet_schema.dump(regmovdet)), 201


# PUT: Actualizar un registro existente
@regmovdet_bp.route('/<int:iddet>', methods=['PUT'])
@jwt_required()
def update_regmovdet(iddet):
    regmovdet = RegMovDet.query.get_or_404(iddet)
    data = request.get_json()

    # Validar los datos de entrada
    errors = regmovdet_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Actualizar los campos del registro
    for key, value in data.items():
        setattr(regmovdet, key, value)

    db.session.commit()
    return jsonify(regmovdet_schema.dump(regmovdet)), 200


# DELETE: Eliminar un registro
@regmovdet_bp.route('/<int:iddet>', methods=['DELETE'])
@jwt_required()
def delete_regmovdet(iddet):
    regmovdet = RegMovDet.query.get_or_404(iddet)
    db.session.delete(regmovdet)
    db.session.commit()
    return jsonify({"message": "Registro eliminado exitosamente"}), 200
