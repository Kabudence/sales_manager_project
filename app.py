from flask import Flask
from extensions import db, migrate, jwt
from auth import auth_bp  # Rutas de autenticación
from routes import crud_bp  # Importar el blueprint principal
from config import Config  # Importar la clase Config

def create_app():
    app = Flask(__name__)

    # Configuración usando la clase Config
    app.config.from_object(Config)  # Aquí se aplica la configuración desde la clase Config

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(crud_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Crea las tablas si aún no existen
    app.run(debug=True)
