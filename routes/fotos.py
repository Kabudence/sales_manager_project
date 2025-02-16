import base64
import traceback

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from extensions import db
from models import FotoProductoVendido, RegMovDet, Producto

fotos_bp = Blueprint('fotos_bp', __name__)



@fotos_bp.route('/upload-photo', methods=['POST'])
@jwt_required()
def upload_photo():
    try:
        # LOG: Leer el body JSON
        data = request.get_json()
        regmovdet_id = data.get('regmovdet_id')
        foto_base64 = data.get('foto_codigo')


        # Verificar parámetros
        if not regmovdet_id or not foto_base64:
            return jsonify({'error': 'Faltan datos: regmovdet_id o foto_codigo'}), 400

        # LOG: Revisar si existe el regmovdet en la DB
        regmovdet = RegMovDet.query.get(regmovdet_id)
        if not regmovdet:
            return jsonify({'error': f'No existe regmovdet_id {regmovdet_id}'}), 404

        # LOG: Crear objeto FotoProductoVendido
        nueva_foto = FotoProductoVendido(
            regmovdet_id=regmovdet_id,
            foto_codigo=foto_base64
        )

        # LOG: Agregar y confirmar en DB
        db.session.add(nueva_foto)
        db.session.commit()

        return jsonify({
            'message': 'Foto guardada con éxito',
            'foto_id': nueva_foto.id
        }), 201

    except Exception as e:
        db.session.rollback()


        traceback.print_exc()

        return jsonify({'error': str(e)}), 500

@fotos_bp.route('/by-idcab/<int:idcab>', methods=['GET'])
@jwt_required()
def get_fotos_by_idcab(idcab):
    """
    Obtiene las fotos asociadas a un idcab con paginación.
    Se pueden enviar los parámetros query 'limit' (por defecto 1) y 'offset' (por defecto 0).
    """
    try:
        limit = int(request.args.get('limit', 1))
        offset = int(request.args.get('offset', 0))

        fotos = db.session.query(
            FotoProductoVendido.id,
            FotoProductoVendido.regmovdet_id,
            FotoProductoVendido.foto_codigo,
            FotoProductoVendido.fecha,
            Producto.nomproducto,
            RegMovDet.total,
            RegMovDet.cantidad
        ).join(
            RegMovDet, FotoProductoVendido.regmovdet_id == RegMovDet.iddet
        ).join(
            Producto, RegMovDet.producto == Producto.idprod
        ).filter(
            RegMovDet.idcab == idcab
        ).order_by(FotoProductoVendido.fecha.asc()) \
         .limit(limit).offset(offset) \
         .all()

        resultado = []
        for foto in fotos:
            resultado.append({
                "id": foto.id,
                "regmovdet_id": foto.regmovdet_id,
                "foto_codigo": foto.foto_codigo,
                "fecha": foto.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "nombre_producto": foto.nomproducto,
                "precio_vendido": foto.total,
                "cantidad": foto.cantidad
            })

        # También podrías incluir información adicional (como total de fotos) si lo deseas.
        return jsonify({"fotos": resultado}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

