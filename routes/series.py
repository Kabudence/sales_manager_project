from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import Serie, Tienda
from schemas import SerieSchema
from extensions import db

serie_bp = Blueprint('serie_bp', __name__)
serie_schema = SerieSchema()
series_schema = SerieSchema(many=True)

# Obtener todas las series
@serie_bp.route('', methods=['GET'])
@jwt_required()
def get_all_series():
    series = Serie.query.all()
    return jsonify(series_schema.dump(series)), 200

# Obtener una serie específica
@serie_bp.route('/<string:tcomp>/<string:serie>', methods=['GET'])
@jwt_required()
def get_serie(tcomp, serie):
    serie_obj = Serie.query.get_or_404((tcomp, serie))
    return jsonify(serie_schema.dump(serie_obj)), 200

# Crear una nueva serie
@serie_bp.route('/', methods=['POST'])
@jwt_required()
def create_serie():
    data = request.get_json()

    # Validar datos
    errors = serie_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Verificar si la tienda existe
    tienda = Tienda.query.get(data['idemp'])
    if not tienda:
        return jsonify({"error": "La tienda especificada no existe"}), 404

    # Crear la nueva serie
    serie = Serie(**data)
    db.session.add(serie)
    db.session.commit()
    return jsonify(serie_schema.dump(serie)), 201

# Actualizar una serie
@serie_bp.route('/<string:tcomp>/<string:serie>', methods=['PUT'])
@jwt_required()
def update_serie(tcomp, serie):
    serie_obj = Serie.query.get_or_404((tcomp, serie))
    data = request.get_json()

    # Validar datos
    errors = serie_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Verificar si la tienda existe
    if 'idemp' in data:
        tienda = Tienda.query.get(data['idemp'])
        if not tienda:
            return jsonify({"error": "La tienda especificada no existe"}), 404

    # Actualizar los campos de la serie
    for key, value in data.items():
        setattr(serie_obj, key, value)

    db.session.commit()
    return jsonify(serie_schema.dump(serie_obj)), 200

# Eliminar una serie
@serie_bp.route('/<string:tcomp>/<string:serie>', methods=['DELETE'])
@jwt_required()
def delete_serie(tcomp, serie):
    serie_obj = Serie.query.get_or_404((tcomp, serie))
    db.session.delete(serie_obj)
    db.session.commit()
    return jsonify({"message": "Serie eliminada exitosamente"}), 200
