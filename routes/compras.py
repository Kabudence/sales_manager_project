from flask import Blueprint, request, jsonify
from models import Compra
from extensions import db
from schemas import CompraSchema

compra_bp = Blueprint('compra_bp', __name__)
compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)

@compra_bp.route('/compras', methods=['GET'])
def get_all_compras():
    compras = Compra.query.all()
    return jsonify(compras_schema.dump(compras)), 200

@compra_bp.route('/compras/<int:id>', methods=['GET'])
def get_compra(id):
    compra = Compra.query.get_or_404(id)
    return jsonify(compra_schema.dump(compra)), 200

@compra_bp.route('/compras', methods=['POST'])
def create_compra():
    data = request.get_json()
    compra = Compra(**data)
    db.session.add(compra)
    db.session.commit()
    return jsonify(compra_schema.dump(compra)), 201

@compra_bp.route('/compras/<int:id>', methods=['PUT'])
def update_compra(id):
    compra = Compra.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(compra, key, value)
    db.session.commit()
    return jsonify(compra_schema.dump(compra)), 200

@compra_bp.route('/compras/<int:id>', methods=['DELETE'])
def delete_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()
    return jsonify({"message": "Compra eliminada exitosamente"}), 200
