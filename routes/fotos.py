import base64
import traceback

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from extensions import db
from models import FotoProductoVendido, RegMovDet, Producto

fotos_bp = Blueprint('fotos_bp', __name__)



@fotos_bp.route('/upload-photo', methods=['POST'])
def upload_photo():
    try:
        # LOG: Leer el body JSON
        data = request.get_json()
        regmovdet_id = data.get('regmovdet_id')
        foto_base64 = data.get('foto_codigo')

        # LOG: Imprimir lo que estamos recibiendo
        print(f"[DEBUG] /upload-photo => regmovdet_id={regmovdet_id}, foto_base64 length={(len(foto_base64) if foto_base64 else 0)}")

        # Verificar parámetros
        if not regmovdet_id or not foto_base64:
            print("[DEBUG] /upload-photo => Faltan datos regmovdet_id o foto_codigo.")
            return jsonify({'error': 'Faltan datos: regmovdet_id o foto_codigo'}), 400

        # LOG: Revisar si existe el regmovdet en la DB
        regmovdet = RegMovDet.query.get(regmovdet_id)
        if not regmovdet:
            print(f"[DEBUG] /upload-photo => No existe regmovdet_id={regmovdet_id} en RegMovDet.")
            return jsonify({'error': f'No existe regmovdet_id {regmovdet_id}'}), 404

        # LOG: Crear objeto FotoProductoVendido
        print(f"[DEBUG] Creando FotoProductoVendido => regmovdet_id={regmovdet_id}")
        nueva_foto = FotoProductoVendido(
            regmovdet_id=regmovdet_id,
            foto_codigo=foto_base64
        )

        # LOG: Agregar y confirmar en DB
        db.session.add(nueva_foto)
        db.session.commit()

        print(f"[DEBUG] Foto guardada con éxito => foto_id={nueva_foto.id}")
        return jsonify({
            'message': 'Foto guardada con éxito',
            'foto_id': nueva_foto.id
        }), 201

    except Exception as e:
        # LOG: en caso de error 500, revirtiendo transacción
        db.session.rollback()

        # LOG: imprimir traceback completo en consola
        print("[ERROR] Ocurrió una excepción en /upload-photo:")
        traceback.print_exc()

        return jsonify({'error': str(e)}), 500

@fotos_bp.route('/by-idcab/<int:idcab>', methods=['GET'])
def get_fotos_by_idcab(idcab):
    """
    Obtiene todas las fotos asociadas a un idcab específico,
    haciendo un JOIN con regmovdet y productos para incluir información adicional.
    """
    try:
        # Realizar el JOIN entre FotoProductoVendido, regmovdet y productos
        fotos = db.session.query(
            FotoProductoVendido.id,
            FotoProductoVendido.regmovdet_id,
            FotoProductoVendido.foto_codigo,
            FotoProductoVendido.fecha,
            Producto.nomproducto,  # Nombre del producto
            RegMovDet.total,
            RegMovDet.cantidad# Precio vendido
        ).join(
            RegMovDet,
            FotoProductoVendido.regmovdet_id == RegMovDet.iddet
        ).join(
            Producto,
            RegMovDet.producto == Producto.idprod
        ).filter(
            RegMovDet.idcab == idcab
        ).all()

        # Convertir los resultados a JSON
        resultado = []
        for foto in fotos:
            resultado.append({
                "id": foto.id,
                "regmovdet_id": foto.regmovdet_id,
                "foto_codigo": foto.foto_codigo,  # Base64
                "fecha": foto.fecha.strftime("%Y-%m-%d %H:%M:%S"),  # Formatear la fecha
                "nombre_producto": foto.nomproducto,  # Nombre del producto
                "precio_vendido": foto.total,         # Precio vendido
                "cantidad": foto.cantidad         # Precio vendido
            })

        return jsonify({"fotos": resultado}), 200

    except Exception as e:
        db.session.rollback()
        print("[ERROR] Ocurrió una excepción en GET /fotos/by-idcab/<idcab>:")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
