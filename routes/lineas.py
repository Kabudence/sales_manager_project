from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Linea
from schemas import LineaSchema
from extensions import db

linea_bp = Blueprint('linea_bp', __name__)
linea_schema = LineaSchema()
lineas_schema = LineaSchema(many=True)

@linea_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_lineas():
    lineas = Linea.query.all()
    return jsonify(lineas_schema.dump(lineas)), 200

@linea_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_linea(id):
    linea = Linea.query.get_or_404(id)
    return jsonify(linea_schema.dump(linea)), 200

@linea_bp.route('', methods=['POST'])
@jwt_required()
def create_linea():
    linea = linea_schema.load(request.json)
    data = request.get_json()
    errors = linea_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    linea = Linea(**data)
    db.session.add(linea)
    db.session.commit()
    return jsonify(linea_schema.dump(linea)), 201

@linea_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_linea(id):
    linea = Linea.query.get_or_404(id)
    data = request.get_json()
    errors = linea_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(linea, key, value)
    db.session.commit()
    return jsonify(linea_schema.dump(linea)), 200

@linea_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_linea(id):
    linea = Linea.query.get_or_404(id)
    db.session.delete(linea)
    db.session.commit()
    return jsonify({"message": "Linea eliminada exitosamente"}), 200

@linea_bp.route('/api/lineas/<int:idlinea>/productos', methods=['GET'])
@jwt_required()
def get_productos_por_linea(idlinea):
    linea = Linea.query.get_or_404(idlinea)
    productos = linea.productos.all()  # Obtiene los productos relacionados
    return jsonify([producto.nomproducto for producto in productos])
