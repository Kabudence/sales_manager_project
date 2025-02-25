from flask_bcrypt import Bcrypt
from extensions import db
from enum import Enum
from sqlalchemy.dialects.mysql import ENUM


bcrypt = Bcrypt()


class UserRole(Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default=UserRole.EMPLOYEE.value, nullable=False)  # Almacena el valor del rol como cadena

    def __init__(self, username, password, role=UserRole.EMPLOYEE.value):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

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

    idemp = db.Column(db.String(10), nullable=False)  # Empresa relacionada
    periodo = db.Column(db.String(10), nullable=False)  # Periodo del producto
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
    estado = db.Column(db.Integer, db.ForeignKey('tipo_estados.tipo_estado_id'))

    def __repr__(self):
        return f"<Producto {self.idprod}>"



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

    idlinea = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

#
# class Venta(db.Model):
#     __tablename__ = 'vista_ventas'
#     __table_args__ = {'extend_existing': True}  # Permitir uso sobre vistas
#
#     fecha = db.Column(db.Date, nullable=False)
#     tipo_movimiento = db.Column(db.String(50), nullable=False)
#     tipo_venta = db.Column(db.String(50), nullable=False)
#     num_docum = db.Column(db.String(50), nullable=False)
#     ruc_cliente = db.Column(db.String(20), nullable=False)
#     cliente = db.Column(db.String(100), nullable=False)
#     valor_de_venta = db.Column(db.Float, nullable=False)
#     igv = db.Column(db.Float, nullable=False)
#     total = db.Column(db.Float, nullable=False)
#     estado = db.Column(db.String(10), nullable=False)
#



class TipoEstados(db.Model):
    __tablename__ = 'tipo_estados'

    tipo_estado_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)




class Compra(db.Model):
    __tablename__ = 'vista_compras'  # Nombre de la vista en la base de datos
    fecha = db.Column(db.Date, nullable=False)
    tipo_movimiento = db.Column(db.String(100), nullable=False)
    tipo_venta = db.Column(db.String(100), nullable=False)
    num_docum = db.Column(db.String(50), nullable=False, primary_key=True)
    ruc_cliente = db.Column(db.String(20), nullable=False)
    proveedor = db.Column(db.String(100), nullable=False)
    valor_de_venta = db.Column(db.String(100), nullable=False)
    igv = db.Column(db.String(100), nullable=False)
    total = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)



class RegMovCab(db.Model):
    __tablename__ = 'regmovcab'

    idmov = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Identificador único
    fecha = db.Column(db.Date, nullable=False)  # Fecha de la operación
    tip_mov = db.Column(db.String(10), nullable=False)  # Tipo de movimiento (ej. venta/compra)
    tip_vta = db.Column(db.String(10), nullable=False)  # Tipo de venta
    tip_docum = db.Column(db.String(10), nullable=False)  # Tipo de documento (ej. factura/boleta)
    num_docum = db.Column(db.String(50), nullable=False)  # Número de documento
    ruc_cliente = db.Column(db.String(15), nullable=False)  # RUC o ID del cliente
    vendedor = db.Column(db.String(50), nullable=True)  # Nombre del vendedor
    vvta = db.Column(db.Float, nullable=False)  # Valor de la venta
    igv = db.Column(db.Float, nullable=False)  # Impuesto General a las Ventas
    total = db.Column(db.Float, nullable=False)  # Total de la operación
    idemp = db.Column(db.String(10), nullable=False)  # Identificador de la empresa
    estado = db.Column(db.String(10), nullable=False)  # Estado de la transacción



class RegMovDet(db.Model):
    __tablename__ = 'regmovdet'

    iddet = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID autogenerado
    idcab = db.Column(db.Integer)
    producto = db.Column(db.String(8), nullable=False)  # Código del producto
    cantidad = db.Column(db.Numeric(12, 2), nullable=False)  # Cantidad del producto
    precio = db.Column(db.Numeric(12, 2), nullable=False)  # Precio unitario
    igv = db.Column(db.Numeric(12, 2), nullable=False)  # IGV
    total = db.Column(db.Numeric(12, 2), nullable=False)  # Total
    st_act = db.Column(db.Numeric(12, 2), nullable=False)  # Estado actual (puede ser stock u otro valor)

    def __repr__(self):
        return f"<RegMovDet iddet={self.iddet}, idcab={self.idcab}, producto={self.producto}>"



class FotoProductoVendido(db.Model):
    __tablename__ = 'foto_producto_vendido'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    regmovdet_id = db.Column(db.Integer)
    foto_codigo = db.Column(db.Text, nullable=False)  # Aquí se almacenará la imagen en Base64
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<FotoProductoVendido {self.id}>"



class Notificacion(db.Model):
    __tablename__ = "notificaciones"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('leido', 'no_leido'), nullable=False, default='no_leido')
    numdocum_regmovcab = db.Column(db.String(50), nullable=False)  # Nuevo campo obligatorio
