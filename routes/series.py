from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Serie
from schemas import SerieSchema
from extensions import db

serie_bp = Blueprint('serie_bp', __name__)
serie_schema = SerieSchema()
series_schema = SerieSchema(many=True)

@serie_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_series():
    series = Serie.query.all()
    return jsonify(series_schema.dump(series)), 200

@serie_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_serie(id):
    serie = Serie.query.get_or_404(id)
    return jsonify(serie_schema.dump(serie)), 200

@serie_bp.route('/', methods=['POST'])
@jwt_required()
def create_serie():
    data = request.get_json()
    errors = serie_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    serie = Serie(**data)
    db.session.add(serie)
    db.session.commit()
    return jsonify(serie_schema.dump(serie)), 201

@serie_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_serie(id):
    serie = Serie.query.get_or_404(id)
    data = request.get_json()
    errors = serie_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(serie, key, value)
    db.session.commit()
    return jsonify(serie_schema.dump(serie)), 200

@serie_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_serie(id):
    serie = Serie.query.get_or_404(id)
    db.session.delete(serie)
    db.session.commit()
    return jsonify({"message": "Serie eliminada exitosamente"}), 200
