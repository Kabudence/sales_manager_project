from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
import json  # Asegúrate de importar este módulo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from extensions import db
from models import User, UserRole

# Configuración de seguridad adicional
limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"])

auth_bp = Blueprint('auth', __name__)

# Ruta para registrar usuarios
@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")  # Limita la cantidad de registros por minuto
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', UserRole.EMPLOYEE.value)  # Rol por defecto: EMPLOYEE

        if role not in [e.value for e in UserRole]:
            return jsonify({"error": "Rol inválido"}), 400

        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "El usuario ya existe"}), 400

        # Crear el nuevo usuario
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Limita la cantidad de intentos de inicio de sesión por minuto
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Serializamos el objeto de identidad
        identity = json.dumps({"username": user.username, "role": user.role})
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401

# Ruta para refrescar tokens
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Aquí usamos el decorador actualizado
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")  # Limita la cantidad de accesos a esta ruta
def protected():
    # Deserializamos el objeto de identidad
    current_user = json.loads(get_jwt_identity())
    return jsonify(logged_in_as=current_user), 200


@auth_bp.route('/admin-only', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()

    # Asegúrate de que current_user sea un diccionario
    if isinstance(current_user, str):
        import json
        current_user = json.loads(current_user)

    if current_user.get("role") != UserRole.ADMIN.value:
        return jsonify({"msg": "No tienes permiso para acceder a esta ruta"}), 403

    return jsonify({"msg": "Acceso concedido para administradores"}), 200
