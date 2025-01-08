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
    __tablename__ = 'clientes'  # Cambia a 'clientes'

    idcliente = db.Column(db.String(50), primary_key=True)  # Ajusta según el campo de la base de datos
    tdoc = db.Column(db.String(50), nullable=False)
    nomcliente = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)

class Proveedor(db.Model):
    __tablename__ = 'proveedor'  # Asegúrate de que el nombre coincide con tu tabla

    ruc = db.Column(db.String(50), primary_key=True)  # Según el campo `ruc` de la tabla
    nomproveedor = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    celular = db.Column(db.String(20))  # Este campo es opcional
    contacto = db.Column(db.String(100))  # Contacto adicional opcional
    correo = db.Column(db.String(100))  # Email del proveedor
    estado = db.Column(db.String(10), default="ACTIVO")  # Estado del proveedor



class Producto(db.Model):
    __tablename__ = 'productos'

    idprod = db.Column(db.String(50), primary_key=True)
    nomproducto = db.Column(db.String(100), nullable=False)
    umedida = db.Column(db.String(20), nullable=False)
    st_ini = db.Column(db.Integer, default=0)
    st_act = db.Column(db.Integer, default=0)
    st_min = db.Column(db.Integer, default=0)
    pr_costo = db.Column(db.Float, nullable=False)
    prventa = db.Column(db.Float, nullable=False)
    modelo = db.Column(db.String(50), nullable=True)
    medida = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(10), nullable=False)

    # Elimina idlinea porque no existe en la base de datos


class Vendedor(db.Model):
    __tablename__ = 'vendedor'

    idvend = db.Column(db.Integer, primary_key=True)
    nomvendedor = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    idemp = db.Column(db.Integer, db.ForeignKey('tiendas.idemp'), nullable=False)
    estado = db.Column(db.String(10), nullable=False)

    # Relación con Tienda
    tienda = db.relationship('Tienda', backref='vendedores')

from extensions import db

class Serie(db.Model):
    __tablename__ = 'ncorrela'

    tcomp = db.Column(db.String(10), primary_key=True)  # Tipo de comprobante
    serie = db.Column(db.String(10), primary_key=True)  # Serie
    numero = db.Column(db.Integer, nullable=False)      # Número correlativo
    idemp = db.Column(db.Integer, db.ForeignKey('tiendas.idemp'), nullable=False)  # Tienda relacionada

    # Relación con Tienda
    tienda = db.relationship('Tienda', backref='series')


class Linea(db.Model):
    __tablename__ = 'lineas'

    idlinea = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    idemp = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.Integer, nullable=False)

class Clase(db.Model):
    __tablename__ = 'clases'

    idclase = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(255), nullable=False)
    idemp = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(10), nullable=False)

class Tienda(db.Model):
    __tablename__ = 'tiendas'  # Asegúrate de que coincida con el nombre de la tabla
    idemp = db.Column(db.String(50), primary_key=True)  # Columna idemp en la tabla
    nombree = db.Column(db.String(100), nullable=False)  # Columna nombree en la tabla

    def __repr__(self):
        return f"<Tienda idemp={self.idemp} nombree={self.nombree}>"


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


from extensions import db

class Compra(db.Model):
    __tablename__ = 'regmovcab'  # Nombre de la tabla en la base de datos

    idmov = db.Column(db.Integer, primary_key=True)  # ID único
    fecha = db.Column(db.Date, nullable=False)  # Fecha de la compra
    tip_mov = db.Column(db.String(50), nullable=False)  # Tipo de movimiento
    tip_vta = db.Column(db.String(50), nullable=False)  # Tipo de venta
    tip_docum = db.Column(db.String(50), nullable=False)  # Tipo de documento
    num_docum = db.Column(db.String(50), nullable=False)  # Número del documento
    ruc_cliente = db.Column(db.String(11), nullable=False)  # RUC del cliente
    vendedor = db.Column(db.String(100), nullable=False)  # Vendedor
    vvta = db.Column(db.Float, nullable=False)  # Valor de la venta
    igv = db.Column(db.Float, nullable=False)  # IGV (Impuesto General a las Ventas)
    total = db.Column(db.Float, nullable=False)  # Total de la compra
    idemp = db.Column(db.Integer, nullable=False)  # ID de la empresa
    estado = db.Column(db.String(50), nullable=False)  # Estado de la compra
