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
        data = request.json
        regmovdet_id = data.get('regmovdet_id')
        foto_base64 = data.get('foto')

        if not regmovdet_id or not foto_base64:
            return jsonify({'error': 'Faltan datos: regmovdet_id o foto'}), 400

        # Decodificar la foto de base64 a binario
        foto_binaria = base64.b64decode(foto_base64)

        # Crear un nuevo registro en la tabla foto_producto_vendido
        nueva_foto = FotoProductoVendido(
            regmovdet_id=regmovdet_id
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