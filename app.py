from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from extensions import db, migrate, jwt
from config import Config
from flask_cors import CORS

from routes import proveedor_bp, producto_bp, linea_bp, clase_bp, tienda_bp, vendedor_bp, serie_bp,auth_bp
from routes.clientes import cliente_bp
from routes.compras import compra_bp
from routes.regmovcab import regmovcab_bp
from routes.ventas import venta_bp

jwt = JWTManager()

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

    app.register_blueprint(cliente_bp, url_prefix="/api/clientes")
    app.register_blueprint(proveedor_bp, url_prefix="/api/proveedores")
    app.register_blueprint(linea_bp, url_prefix='/api/lineas')
    app.register_blueprint(clase_bp, url_prefix='/api/clases')
    app.register_blueprint(tienda_bp, url_prefix='/api/tiendas')
    app.register_blueprint(vendedor_bp, url_prefix='/api/vendedores')
    app.register_blueprint(serie_bp, url_prefix='/api/series')
    app.register_blueprint(regmovcab_bp, url_prefix='/api/regmovcab')
    app.register_blueprint(compra_bp, url_prefix='/api/compras')
    app.register_blueprint(venta_bp, url_prefix='/api/ventas')
    app.register_blueprint(producto_bp, url_prefix="/api/productos")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            headers = response.headers

            # Asegúrate de que los encabezados necesarios estén presentes
            headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response

    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        print(f"[JWT] Unauthorized callback activado. Razón: {reason}")
        return jsonify({"msg": "No autorizado", "reason": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        print(f"[JWT] Invalid token callback activado. Razón: {reason}")
        return jsonify({"msg": "Token inválido", "reason": reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"[JWT] Expired token callback activado. JWT: {jwt_payload}")
        return jsonify({"msg": "El token ha expirado"}), 401

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
