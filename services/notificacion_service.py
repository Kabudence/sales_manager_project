from extensions import db
from models import Notificacion

def crear_notificacion(descripcion, estado='no_leido', numdocum_regmovcab=None):
    """
    Función para crear una notificación en la base de datos.
    Esta función puede ser utilizada en cualquier endpoint sin exponer un endpoint directo.

    Args:
        descripcion (str): Descripción de la notificación. Obligatorio.
        estado (str): Estado inicial de la notificación ('leido' o 'no_leido'). Por defecto, 'no_leido'.
        numdocum_regmovcab (str): Número de documento del registro asociado en regmovcab. Obligatorio.

    Returns:
        dict: Mensaje de éxito y datos de la notificación creada.

    Raises:
        ValueError: Si falta el campo 'descripcion' o 'numdocum_regmovcab'.
    """
    try:
        if not descripcion:
            raise ValueError("El campo 'descripcion' es obligatorio.")
        if not numdocum_regmovcab:
            raise ValueError("El campo 'numdocum_regmovcab' es obligatorio.")

        nueva_notificacion = Notificacion(
            descripcion=descripcion,
            estado=estado,
            numdocum_regmovcab=numdocum_regmovcab  # Asociar al registro regmovcab
        )
        db.session.add(nueva_notificacion)
        db.session.commit()

        return {
            "message": "Notificación creada con éxito",
            "notificacion": {
                "id": nueva_notificacion.id,
                "descripcion": nueva_notificacion.descripcion,
                "estado": nueva_notificacion.estado,
                "numdocum_regmovcab": nueva_notificacion.numdocum_regmovcab
            }
        }
    except Exception as e:
        db.session.rollback()
        raise e  # Relanzar la excepción para que el endpoint que llame esta función la maneje
