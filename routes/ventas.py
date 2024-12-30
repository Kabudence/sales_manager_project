from flask import Blueprint, request, jsonify
from models import Venta
from extensions import db
from schemas import VentaSchema

venta_bp = Blueprint('venta_bp', __name__)
venta_schema = VentaSchema()
ventas_schema = VentaSchema(many=True)

@venta_bp.route('/ventas', methods=['GET'])
def get_all_ventas():
    ventas = Venta.query.all()
    return jsonify(ventas_schema.dump(ventas)), 200

@venta_bp.route('/ventas/<int:id>', methods=['GET'])
def get_venta(id):
    venta = Venta.query.get_or_404(id)
    return jsonify(venta_schema.dump(venta)), 200

@venta_bp.route('/ventas', methods=['POST'])
def create_venta():
    data = request.get_json()
    venta = Venta(**data)
    db.session.add(venta)
    db.session.commit()
    return jsonify(venta_schema.dump(venta)), 201

@venta_bp.route('/ventas/<int:id>', methods=['PUT'])
def update_venta(id):
    venta = Venta.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(venta, key, value)
    db.session.commit()
    return jsonify(venta_schema.dump(venta)), 200

@venta_bp.route('/ventas/<int:id>', methods=['DELETE'])
def delete_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"message": "Venta eliminada exitosamente"}), 200
