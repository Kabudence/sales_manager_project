from flask import Blueprint, request, jsonify
# Si usas JWT, descomenta:
# from flask_jwt_extended import jwt_required

from models import Producto, Linea, TipoEstados
from schemas import ProductoSchema
from extensions import db

producto_bp = Blueprint('producto_bp', __name__)

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)


@producto_bp.route('/', methods=['POST'])
def create_producto():
    data = request.get_json()

    # Validar campos requeridos
    required_fields = ["idprod", "nomproducto", "umedida"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"El campo {field} es obligatorio"}), 400

    # Validar la línea asociada
    linea_id = data.get("idprod")[:2]  # Ejemplo: usa los primeros dos dígitos para obtener la línea
    linea = Linea.query.filter_by(idlinea=linea_id).first()
    if not linea:
        return jsonify({"error": f"La línea con ID {linea_id} no existe"}), 404

    # Crear el producto
    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()

    return jsonify({"message": "Producto creado con éxito", "producto": producto.idprod}), 201




@producto_bp.route('/<string:id>', methods=['GET'])
# @jwt_required()
def get_producto(id):
    """
    GET /api/productos/<id>
    """
    producto = Producto.query.get_or_404(id)
    return jsonify(producto_schema.dump(producto)), 200
@producto_bp.route('/', methods=['GET'])
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
def update_producto(idprod):
    data = request.get_json()

    # Validar que el producto exista
    producto = Producto.query.get(idprod)
    if not producto:
        return jsonify({"error": f"El producto con id {idprod} no existe"}), 404

    # Validar que la línea exista si se proporciona
    idlinea = data.get("idlinea")
    if idlinea:
        linea = Linea.query.get(idlinea)
        if not linea:
            return jsonify({"error": f"La línea con id {idlinea} no existe"}), 404

    # Actualizar los campos
    for key, value in data.items():
        setattr(producto, key, value)

    db.session.commit()

    return jsonify({"message": "Producto actualizado con éxito", "producto": producto.idprod}), 200

# Opcionalmente, ruta DELETE:
@producto_bp.route('/<string:id>', methods=['DELETE'])
# @jwt_required()
def delete_producto(id):
    """
    DELETE /api/productos/<id>
    """
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200
