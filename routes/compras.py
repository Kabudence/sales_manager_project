from flask import Blueprint, request, jsonify
from sqlalchemy import text
from models import Compra
from schemas import CompraSchema
from extensions import db

compra_bp = Blueprint('compra_bp', __name__)
compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)

@compra_bp.route('/', methods=['GET'])
def get_compras():
    try:
        # Obtener parámetros de la solicitud
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        offset = (page - 1) * size

        # Consulta SQL con paginación
        query = text(f"SELECT * FROM vista_compras LIMIT {size} OFFSET {offset}")
        total_query = text("SELECT COUNT(*) FROM vista_compras")

        with db.engine.connect() as connection:
            result = connection.execute(query)
            total_result = connection.execute(total_query)
            compras = [dict(row._mapping) for row in result]
            total_compras = total_result.scalar()  # Total de registros

        # Calcular número total de páginas
        total_pages = (total_compras + size - 1) // size

        # Devolver la respuesta con paginación
        return jsonify({
            "items": compras,
            "totalPages": total_pages,
            "currentPage": page,
            "pageSize": size
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@compra_bp.route('/<string:num_docum>', methods=['GET'])
def get_compra_by_num_docum(num_docum):
    try:
        compra = Compra.query.filter_by(num_docum=num_docum).first_or_404()
        return jsonify(compra_schema.dump(compra)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@compra_bp.route('/advanced-search', methods=['GET'])
def advanced_search_compras():
    try:
        # Parámetros de búsqueda
        from_price = request.args.get('fromPrice')
        to_price = request.args.get('toPrice')
        proveedor = request.args.get('providerName')
        from_date = request.args.get('fromDate')
        to_date = request.args.get('toDate')
        sale_type = request.args.get('saleType')
        ruc_cliente = request.args.get('clientRUC')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        offset = (page - 1) * size

        # Construir consulta dinámica
        base_query = "SELECT * FROM vista_compras WHERE 1=1"
        count_query = "SELECT COUNT(*) FROM vista_compras WHERE 1=1"
        filters = []

        if from_price:
            base_query += " AND valor_de_venta >= :from_price"
            count_query += " AND valor_de_venta >= :from_price"
            filters.append(("from_price", from_price))

        if to_price:
            base_query += " AND valor_de_venta <= :to_price"
            count_query += " AND valor_de_venta <= :to_price"
            filters.append(("to_price", to_price))

        if proveedor:
            base_query += " AND proveedor LIKE :proveedor"
            count_query += " AND proveedor LIKE :proveedor"
            filters.append(("proveedor", f"%{proveedor}%"))

        if from_date:
            base_query += " AND fecha >= :from_date"
            count_query += " AND fecha >= :from_date"
            filters.append(("from_date", from_date))

        if to_date:
            base_query += " AND fecha <= :to_date"
            count_query += " AND fecha <= :to_date"
            filters.append(("to_date", to_date))

        if sale_type:
            base_query += " AND tipo_venta = :sale_type"
            count_query += " AND tipo_venta = :sale_type"
            filters.append(("sale_type", sale_type))

        if ruc_cliente:
            base_query += " AND ruc_cliente = :ruc_cliente"
            count_query += " AND ruc_cliente = :ruc_cliente"
            filters.append(("ruc_cliente", ruc_cliente))

        if status:
            base_query += " AND estado = :status"
            count_query += " AND estado = :status"
            filters.append(("status", status))

        # Agregar paginación y orden
        base_query += " ORDER BY fecha DESC LIMIT :size OFFSET :offset"

        filters.append(("size", size))
        filters.append(("offset", offset))

        # Ejecutar consultas
        with db.engine.connect() as connection:
            result = connection.execute(text(base_query), dict(filters))
            total_result = connection.execute(text(count_query), dict(filters))

            compras = [dict(row._mapping) for row in result]
            total_compras = total_result.scalar()

        # Calcular páginas totales
        total_pages = (total_compras + size - 1) // size

        return jsonify({
            "items": compras,
            "totalPages": total_pages,
            "currentPage": page,
            "pageSize": size,
            "total": total_compras
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
