from flask import Flask, request, jsonify
from flask_cors import CORS
from extensions import db, migrate, jwt
from config import Config

# Importar blueprints
from routes import proveedor_bp, producto_bp, linea_bp, clase_bp, tienda_bp, vendedor_bp, serie_bp, auth_bp
from routes.clientes import cliente_bp
from routes.compras import compra_bp
from routes.notificaciones import notificaciones_bp
from routes.regmovcab import regmovcab_bp
from routes.regmovdet import regmovdet_bp
from routes.ventas import venta_bp
from routes.fotos import fotos_bp
from routes.utilidades import utilidades_bp

# Para la tarea automática de eliminación de imágenes
from apscheduler.schedulers.background import BackgroundScheduler
from services.cleanup import eliminar_fotos_antiguas

# 1) Define la aplicación de Flask globalmente
app = Flask(__name__)
app.config.from_object(Config)

# 2) Inicializar las extensiones
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# 3) Programar la tarea de limpieza de fotos
scheduler = BackgroundScheduler()
scheduler.add_job(eliminar_fotos_antiguas, 'interval', days=1)
scheduler.start()


# 4) Configurar CORS sobre la instancia global `app`
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173","https://web-production-927a.up.railway.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
    }
})

# 5) Registrar todos los blueprints
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
app.register_blueprint(fotos_bp, url_prefix='/api/fotos')
app.register_blueprint(notificaciones_bp, url_prefix='/api/notificaciones')
app.register_blueprint(regmovdet_bp, url_prefix='/api/regmovdet')
app.register_blueprint(utilidades_bp, url_prefix='/api/utilidades')

# 6) Manejar las solicitudes OPTIONS (CORS preflight)
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        headers = response.headers
        headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
        headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response


# 7) Manejo de errores de JWT
@jwt.unauthorized_loader
def unauthorized_callback(reason):
    return jsonify({"msg": "No autorizado", "reason": reason}), 401

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return jsonify({"msg": "Token inválido", "reason": reason}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "El token ha expirado"}), 401

# 8) Inicio de la aplicación en modo local
if __name__ == '__main__':
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    # Ejecutar Flask en modo debug
    app.run(debug=True)
