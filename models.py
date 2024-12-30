from flask_bcrypt import Bcrypt
from extensions import db

bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(10), default="ACTIVO")

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    contacto = db.Column(db.String(100), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(10), default="ACTIVO")


from extensions import db


class Producto(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad_medida = db.Column(db.String(20), nullable=False)
    stock_inicial = db.Column(db.Integer, default=0)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    precio_costo = db.Column(db.Float, nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    modelo = db.Column(db.String(50), nullable=True)
    medida = db.Column(db.String(50), nullable=True)

    # Clave foránea con nombre explícito
    linea_id = db.Column(db.Integer, db.ForeignKey('linea.id', name='fk_producto_linea'), nullable=False)  # FK a Linea

    # Relación con Linea
    linea = db.relationship('Linea', backref='productos')


class Vendedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(10), default="ACTIVO")

class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comprobante = db.Column(db.String(50), nullable=False)
    serie = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.Integer, nullable=False)

class Linea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(10), default="ACTIVO")

class Clase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(10), default="ACTIVO")

class Tienda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    tipo_movimiento = db.Column(db.String(50), nullable=False)
    tipo_venta = db.Column(db.String(50), nullable=False)
    numero_comprobante = db.Column(db.String(50), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    valor_venta = db.Column(db.Float, nullable=False)
    igv = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default="PROCESADA")

    def __repr__(self):
        return f'<Venta {self.id} - {self.cliente}>'


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    tipo_movimiento = db.Column(db.String(50), nullable=False)
    tipo_compra = db.Column(db.String(50), nullable=False)
    numero_documento = db.Column(db.String(50), nullable=False)
    ruc_proveedor = db.Column(db.String(50), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    igv = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default="PROCESADA")

    def __repr__(self):
        return f'<Compra {self.id} - {self.ruc_proveedor}>'
