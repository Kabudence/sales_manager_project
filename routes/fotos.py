import base64

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from extensions import db
from models import FotoProductoVendido


fotos_bp = Blueprint('fotos_bp', __name__)



@fotos_bp.route('/upload-photo', methods=['POST'])
def upload_photo():
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        regmovdet_id = data.get('regmovdet_id')
        foto_base64 = data.get('foto_codigo')

        if not regmovdet_id or not foto_base64:
            return jsonify({'error': 'Faltan datos: regmovdet_id o foto_codigo'}), 400

        # Verificar si el regmovdet_id existe en la base de datos (opcional)
        from models import RegMovDet
        regmovdet = RegMovDet.query.get(regmovdet_id)
        if not regmovdet:
            return jsonify({'error': f'No existe regmovdet_id {regmovdet_id}'}), 404

        # Crear un nuevo registro en la tabla foto_producto_vendido
        nueva_foto = FotoProductoVendido(
            regmovdet_id=regmovdet_id,
            foto_codigo=foto_base64
        )

        db.session.add(nueva_foto)
        db.session.commit()

        return jsonify({
            'message': 'Foto guardada con éxito',
            'foto_id': nueva_foto.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
