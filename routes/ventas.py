from flask import Blueprint, jsonify
from sqlalchemy import text
from extensions import db

venta_bp = Blueprint('venta_bp', __name__)

# Ruta para obtener todas las ventas
@venta_bp.route('/', methods=['GET'])
def get_all_ventas():
    try:
        query = text("SELECT * FROM vista_ventas")
        with db.engine.connect() as connection:
            result = connection.execute(query)
            ventas = [dict(row._mapping) for row in result]  # Usa ._mapping para convertir filas en dicts
        return jsonify(ventas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener una venta específica por número de documento
@venta_bp.route('/<string:num_docum>', methods=['GET'])
def get_venta_by_num_docum(num_docum):
    try:
        query = text("SELECT * FROM vista_ventas WHERE num_docum = :num_docum")
        with db.engine.connect() as connection:
            result = connection.execute(query, {"num_docum": num_docum})
            venta = result.fetchone()
        if venta:
            return jsonify(dict(venta._mapping)), 200  # Usa ._mapping para convertir filas en dicts
        else:
            return jsonify({"error": "Venta no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
