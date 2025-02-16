from datetime import datetime, timedelta
from flask import current_app
from extensions import db
from sqlalchemy.orm import sessionmaker

def eliminar_fotos_antiguas():
    """Elimina fotos con más de 4 meses de antigüedad en foto_producto_vendido"""
    with current_app.app_context():  # 🔹 Activa el contexto antes de usar `db`
        Session = sessionmaker(bind=db.engine)
        session = Session()

        hace_cuatro_meses = datetime.now() - timedelta(days=90)
        query = "DELETE FROM foto_producto_vendido WHERE fecha < :fecha_limite"
        session.execute(query, {"fecha_limite": hace_cuatro_meses})
        session.commit()

        print("✅ Fotos antiguas eliminadas correctamente")

        session.close()
