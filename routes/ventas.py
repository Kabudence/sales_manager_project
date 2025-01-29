from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from extensions import db

venta_bp = Blueprint('venta_bp', __name__)

# Ruta para obtener todas las ventas
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from extensions import db

venta_bp = Blueprint('venta_bp', __name__)

@venta_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_ventas():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        offset = (page - 1) * size

        query = text(f"""
            SELECT *
            FROM vista_ventas
            ORDER BY fecha DESC
            LIMIT :size OFFSET :offset
        """)

        with db.engine.connect() as connection:
            result = connection.execute(query, {"size": size, "offset": offset})
            ventas = [dict(row._mapping) for row in result]

        count_query = text("SELECT COUNT(*) as total FROM vista_ventas")
        with db.engine.connect() as connection:
            total = connection.execute(count_query).scalar()

        return jsonify({"ventas": ventas, "total": total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener una venta específica por número de documento
@venta_bp.route('/<string:num_docum>', methods=['GET'])
@jwt_required()
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

@venta_bp.route('/advanced-search', methods=['GET'])
# @jwt_required()
def get_advanced_filter_ventas():
    try:
        from_price = request.args.get('fromPrice', type=float)
        to_price = request.args.get('toPrice', type=float)
        client_name = request.args.get('clientName', type=str)
        from_date = request.args.get('fromDate', type=str)
        to_date = request.args.get('toDate', type=str)
        sale_type = request.args.get('saleType', type=str)
        client_ruc = request.args.get('clientRUC', type=str)
        status = request.args.get('status', type=str)
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)

        conditions = ["1=1"]  # Base para filtros dinámicos
        params = {}

        if from_price is not None:
            conditions.append("total >= :from_price")
            params['from_price'] = from_price

        if to_price is not None:
            conditions.append("total <= :to_price")
            params['to_price'] = to_price

        if client_name:
            conditions.append("cliente LIKE :client_name")
            params['client_name'] = f"%{client_name}%"

        if from_date:
            conditions.append("fecha >= :from_date")
            params['from_date'] = from_date

        if to_date:
            conditions.append("fecha <= :to_date")
            params['to_date'] = to_date

        if sale_type:
            conditions.append("tipo_venta = :sale_type")
            params['sale_type'] = sale_type

        if client_ruc:
            conditions.append("ruc_cliente = :client_ruc")
            params['client_ruc'] = client_ruc

        if status:
            conditions.append("estado = :status")
            params['status'] = status

        where_clause = " AND ".join(conditions)
        query = text(f"""
            SELECT *
            FROM vista_ventas
            WHERE {where_clause}
            ORDER BY fecha DESC
            LIMIT :limit OFFSET :offset
        """)

        params['limit'] = limit
        params['offset'] = offset

        with db.engine.connect() as connection:
            result = connection.execute(query, params)
            ventas = [dict(row._mapping) for row in result]  # Convertir filas en dict

        count_query = text(f"SELECT COUNT(*) as total FROM vista_ventas WHERE {where_clause}")
        with db.engine.connect() as connection:
            total = connection.execute(count_query, params).scalar()

        return jsonify({"ventas": ventas, "total": total}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

