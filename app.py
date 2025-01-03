from flask import Flask
from extensions import db, migrate, jwt
from config import Config
from flask_cors import CORS

from routes import proveedor_bp
from routes.clientes import cliente_bp  # Importa tu blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ajustar CORS: permitir orígenes y métodos
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registrar el blueprint con url_prefix="/api/clientes"
    app.register_blueprint(cliente_bp, url_prefix="/api/clientes")
    app.register_blueprint(proveedor_bp, url_prefix="/api/proveedores")

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
