from datetime import datetime, timedelta

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

# Ruta para obtener todas las ventas
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from extensions import db

utilidades_bp = Blueprint('utilidades_bp', __name__)

@utilidades_bp.route('/', methods=['GET'])
def obtener_utilidades():
    """
    Endpoint para obtener utilidades de ventas en un rango de fechas.
    Parámetros:
    - start_date: Fecha de inicio en formato YYYY-MM-DD
    - end_date: Fecha de fin en formato YYYY-MM-DD
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "Se requieren los parámetros 'start_date' y 'end_date'"}), 400

    try:
        query = text("""
            SELECT 
                fecha,
                num_docum,
                vendedor.nomvendedor AS nombre_vendedor,
                vendedor.idvend AS dni_vendedor,
                productos.nomproducto,
                productos.pr_costo * regmovdet.cantidad AS precio_costo,
                regmovdet.total AS precio_venta,
                regmovdet.total - (productos.pr_costo * regmovdet.cantidad) AS utilidades,
                regmovcab.idemp AS empresa
            FROM 
                regmovcab 
            JOIN 
                vendedor ON regmovcab.vendedor = vendedor.idvend
            JOIN
                regmovdet ON regmovcab.idmov = regmovdet.idcab
            JOIN
                productos ON regmovdet.producto = productos.idprod
            WHERE 
                regmovcab.tip_mov = 1 
                AND regmovcab.fecha BETWEEN :start_date AND :end_date;
        """)

        result = db.session.execute(query, {"start_date": start_date, "end_date": end_date})
        ventas = [
            {
                "fecha": row[0],
                "num_docum": row[1],
                "nombre_vendedor": row[2],
                "dni_vendedor": row[3],
                "nomproducto": row[4],
                "precio_costo": float(row[5]),
                "precio_venta": float(row[6]),
                "utilidades": float(row[7]),
                "empresa": row[8]
            }
            for row in result
        ]

        return jsonify({"utilidades": ventas})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@utilidades_bp.route('/empresa', methods=['GET'])
def obtener_utilidades_por_empresa():
    """
    Endpoint para obtener utilidades de ventas en un rango de fechas filtrando por empresa.
    Parámetros:
    - start_date: Fecha de inicio en formato YYYY-MM-DD
    - end_date: Fecha de fin en formato YYYY-MM-DD
    - empresa: Código de empresa (VARCHAR(2))
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    empresa = request.args.get('empresa')

    if not start_date or not end_date or not empresa:
        return jsonify({"error": "Se requieren los parámetros 'start_date', 'end_date' y 'empresa'"}), 400

    try:
        query = text("""
               SELECT 
                   fecha,
                   num_docum,
                   vendedor.nomvendedor AS nombre_vendedor,
                   vendedor.idvend AS dni_vendedor,
                   productos.nomproducto,
                   productos.pr_costo * regmovdet.cantidad AS precio_costo,
                   regmovdet.total AS precio_venta,
                   regmovdet.total - (productos.pr_costo * regmovdet.cantidad) AS utilidades,
                   regmovcab.idemp AS empresa
               FROM 
                   regmovcab 
               JOIN 
                   vendedor ON regmovcab.vendedor = vendedor.idvend
               JOIN
                   regmovdet ON regmovcab.idmov = regmovdet.idcab
               JOIN
                   productos ON regmovdet.producto = productos.idprod
               WHERE 
                   regmovcab.tip_mov = 1 
                   AND regmovcab.fecha BETWEEN :start_date AND :end_date
                   AND regmovcab.idemp = :empresa;
           """)

        result = db.session.execute(query, {"start_date": start_date, "end_date": end_date, "empresa": empresa})
        ventas = [
            {
                "fecha": row[0],
                "num_docum": row[1],
                "nombre_vendedor": row[2],
                "dni_vendedor": row[3],
                "nomproducto": row[4],
                "precio_costo": float(row[5]),
                "precio_venta": float(row[6]),
                "utilidades": float(row[7]),
                "empresa": row[8]
            }
            for row in result
        ]

        return jsonify({"utilidades": ventas})

    except Exception as e:
        return jsonify({"error": str(e)}), 500