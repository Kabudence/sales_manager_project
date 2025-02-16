import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models import Notificacion

# Crear un blueprint para las notificaciones
notificaciones_bp = Blueprint('notificaciones_bp', __name__)

# Endpoint para cambiar el estado de una notificación a 'leído'
@notificaciones_bp.route('/<int:notificacion_id>/leido', methods=['PUT'])
@jwt_required()
def cambiar_a_leido(notificacion_id):
    try:
        # Buscar la notificación en la base de datos
        notificacion = Notificacion.query.get(notificacion_id)

        if not notificacion:
            return jsonify({'error': f'Notificación con id {notificacion_id} no encontrada'}), 404

        # Cambiar el estado a 'leído'
        notificacion.estado = 'leido'
        db.session.commit()

        return jsonify({
            'message': "Estado de la notificación actualizado a 'leído'",
            'notificacion': {
                "id": notificacion.id,
                "descripcion": notificacion.descripcion,
                "estado": notificacion.estado,
                "numdocum_regmovcab": notificacion.numdocum_regmovcab  # Reemplazo de id_regmovcab
            }
        }), 200

    except Exception as e:
        # Revertir la transacción en caso de error
        db.session.rollback()

        # Imprimir el traceback del error
        traceback.print_exc()

        return jsonify({'error': str(e)}), 500


# Endpoint para obtener notificaciones, opcionalmente filtradas por estado y/o numdocum_regmovcab
@notificaciones_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_notificaciones():
    try:
        estado = request.args.get("estado")
        numdocum_regmovcab = request.args.get("numdocum_regmovcab")

        # Validar que el estado sea "leido" o "no_leido" si se proporciona
        if estado and estado not in ["leido", "no_leido"]:
            return jsonify({"error": "El parámetro 'estado' debe ser 'leido' o 'no_leido'"}), 400

        # Construir la consulta base
        query = Notificacion.query

        # Filtrar por estado si se proporciona
        if estado:
            query = query.filter_by(estado=estado)

        # Filtrar por numdocum_regmovcab si se proporciona
        if numdocum_regmovcab:
            query = query.filter_by(numdocum_regmovcab=numdocum_regmovcab)

        # Ejecutar la consulta
        notificaciones = query.all()

        # Convertir los resultados a JSON
        resultado = [
            {
                "id": notificacion.id,
                "descripcion": notificacion.descripcion,
                "estado": notificacion.estado,
                "numdocum_regmovcab": notificacion.numdocum_regmovcab  # Reemplazo de id_regmovcab
            } for notificacion in notificaciones
        ]

        return jsonify({"notificaciones": resultado}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
