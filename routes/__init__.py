from flask import Blueprint

from routes.auth import auth_bp
from routes.clientes import cliente_bp
from routes.proveedores import proveedor_bp
from routes.productos import producto_bp
from routes.vendedores import vendedor_bp
from routes.series import serie_bp
from routes.lineas import linea_bp
from routes.clases import clase_bp
from routes.tiendas import tienda_bp

crud_bp = Blueprint('crud', __name__)

# Registrar sub-blueprints en el blueprint principal
crud_bp.register_blueprint(cliente_bp, url_prefix='/clientes')
crud_bp.register_blueprint(proveedor_bp, url_prefix='/proveedores')
crud_bp.register_blueprint(producto_bp, url_prefix='/productos')
crud_bp.register_blueprint(vendedor_bp, url_prefix='/vendedores')
crud_bp.register_blueprint(serie_bp, url_prefix='/series')
crud_bp.register_blueprint(linea_bp, url_prefix='/lineas')
crud_bp.register_blueprint(clase_bp, url_prefix='/clases')
crud_bp.register_blueprint(tienda_bp, url_prefix='/tiendas')
crud_bp.register_blueprint(auth_bp, url_prefix="/api/auth")

