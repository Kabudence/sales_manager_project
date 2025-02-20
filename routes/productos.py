from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# Si usas JWT, descomenta:
# from flask_jwt_extended import jwt_required

from models import Producto, Linea, TipoEstados
from schemas import ProductoSchema
from extensions import db
from sqlalchemy import func
from unidecode import unidecode

producto_bp = Blueprint('producto_bp', __name__)

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)


@producto_bp.route('', methods=['POST'])
@jwt_required()
def create_producto():
    data = request.get_json()

    # Mapear campos
    mapped_data = {
        "idemp": data.get("idemp", "01"),  # Valor predeterminado
        "periodo": data.get("periodo", "2025"),  # Valor predeterminado
        "idprod": data.get("id"),
        "nomproducto": data.get("nombre"),
        "umedida": data.get("unidad_medida"),
        "st_ini": data.get("stock_inicial", 0),
        "st_act": data.get("stock_actual", 0),
        "st_min": data.get("stock_minimo", 0),
        "pr_costo": data.get("precio_costo", 0.0),
        "prventa": data.get("precio_venta", 0.0),
        "modelo": data.get("modelo", "MODELO"),
        "medida": data.get("medida", "MEDIDA"),
        "estado": data.get("estado", 1),  # Valor predeterminado
    }


    # Validar campos requeridos
    required_fields = ["idprod", "nomproducto", "umedida", "pr_costo", "prventa"]
    for field in required_fields:
        if field not in mapped_data or mapped_data[field] is None:
            return jsonify({"error": f"El campo {field} es obligatorio"}), 400

    # Crear y guardar el producto
    producto = Producto(**mapped_data)
    db.session.add(producto)
    try:
        db.session.commit()
        return jsonify({"message": "Producto creado con éxito", "producto": producto.idprod}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar el producto"}), 500



@producto_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def get_producto(id):
    """
    GET /api/productos/<id>
    """
    producto = Producto.query.get_or_404(id)
    return jsonify(producto_schema.dump(producto)), 200
@producto_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_productos():
    # Consulta con JOIN para incluir el nombre del estado
    productos = db.session.query(
        Producto.idprod,
        Producto.nomproducto,
        Producto.umedida,
        Producto.st_ini,
        Producto.st_act,
        Producto.st_min,
        Producto.pr_costo,
        Producto.prventa,
        Producto.modelo,
        Producto.medida,
        Producto.estado,
        Linea.nombre.label("linea_nombre"),
        TipoEstados.name.label("estado_nombre")
    ).join(
        Linea, Producto.idprod.startswith(Linea.idlinea)
    ).join(
        TipoEstados, Producto.estado == TipoEstados.tipo_estado_id
    ).all()

    # Crear una lista de productos con el estado como nombre
    productos_con_detalles = []
    for producto in productos:
        productos_con_detalles.append({
            "idprod": producto.idprod,
            "nomproducto": producto.nomproducto,
            "umedida": producto.umedida,
            "st_ini": producto.st_ini,
            "st_act": producto.st_act,
            "st_min": producto.st_min,
            "pr_costo": producto.pr_costo,
            "prventa": producto.prventa,
            "modelo": producto.modelo,
            "medida": producto.medida,
            "estado": producto.estado_nombre,  # Usar el nombre del estado
            "linea": producto.linea_nombre if producto.linea_nombre else "Sin Línea"
        })

    return jsonify(productos_con_detalles), 200

@producto_bp.route('/<string:idprod>', methods=['PUT'])
@jwt_required()
def update_producto(idprod):
    data = request.get_json()

    # Validar que el producto exista
    producto = Producto.query.filter_by(idprod=idprod).first()
    if not producto:
        return jsonify({"error": f"El producto con id {idprod} no existe"}), 404

    # Actualizar los campos
    for key, value in data.items():
        if hasattr(producto, key):
            setattr(producto, key, value)

    try:
        db.session.commit()
        return jsonify({"message": "Producto actualizado con éxito", "producto": producto.idprod}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar el producto"}), 500

# Opcionalmente, ruta DELETE:
@producto_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_producto(id):
    """
    DELETE /api/productos/<id>
    """
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200

@producto_bp.route('/search', methods=['GET'])
@jwt_required()
def search_productos():
    term = request.args.get('term', '')
    if not term:
        return jsonify([]), 200

    # Normalizar término de búsqueda
    normalized_term = f"%{unidecode(term).lower()}%"

    # Consulta con joins y filtro
    productos = db.session.query(
        Producto.idprod,
        Producto.nomproducto,
        Producto.umedida,
        Producto.st_ini,
        Producto.st_act,
        Producto.st_min,
        Producto.pr_costo,
        Producto.prventa,
        Producto.modelo,
        Producto.medida,
        Producto.estado,
        Linea.nombre.label("linea_nombre"),
        TipoEstados.name.label("estado_nombre")
    ).join(
        Linea, Producto.idprod.startswith(Linea.idlinea)
    ).join(
        TipoEstados, Producto.estado == TipoEstados.tipo_estado_id
    ).filter(
        func.unaccent(func.lower(Producto.nomproducto)).ilike(func.unaccent(normalized_term))
    ).all()

    # Formatear resultados
    resultados = []
    for p in productos:
        resultados.append({
            "idprod": p.idprod,
            "nomproducto": p.nomproducto,
            "umedida": p.umedida,
            "st_ini": p.st_ini,
            "st_act": p.st_act,
            "st_min": p.st_min,
            "pr_costo": p.pr_costo,
            "prventa": p.prventa,
            "modelo": p.modelo,
            "medida": p.medida,
            "estado": p.estado_nombre,
            "linea": p.linea_nombre or "Sin Línea"
        })

    return jsonify(resultados), 200