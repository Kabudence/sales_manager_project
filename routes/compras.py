from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Compra
from schemas import CompraSchema
from extensions import db

compra_bp = Blueprint('compra_bp', __name__)
compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)

@compra_bp.route('/', methods=['GET'])
# @jwt_required()
def get_all_compras():
    try:
        compras = Compra.query.all()
        return jsonify(compras_schema.dump(compras)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@compra_bp.route('/<string:num_docum>', methods=['GET'])
# @jwt_required()
def get_compra_by_num_docum(num_docum):
    try:
        compra = Compra.query.filter_by(num_docum=num_docum).first_or_404()
        return jsonify(compra_schema.dump(compra)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
