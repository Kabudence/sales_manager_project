from marshmallow import Schema, fields

# Schema para User
class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)

# Schema para Cliente
class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    codigo = fields.Str(required=True)
    nombre = fields.Str(required=True)
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=True)
    estado = fields.Str()


# Schema para Proveedor
class ProveedorSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    codigo = fields.Str(required=True)
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=True)
    contacto = fields.Str()
    correo = fields.Email()
    estado = fields.Str()

# Schema para Producto
class ProductoSchema(Schema):
    id = fields.Str(dump_only=True)
    nombre = fields.Str(required=True)
    unidad_medida = fields.Str(required=True)
    stock_inicial = fields.Int()
    stock_actual = fields.Int()
    stock_minimo = fields.Int()
    precio_costo = fields.Float()
    precio_venta = fields.Float()
    modelo = fields.Str()
    medida = fields.Str()

# Schema para Vendedor
class VendedorSchema(Schema):
    id = fields.Int(dump_only=True)
    codigo = fields.Str(required=True)
    nombre = fields.Str(required=True)
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=True)
    correo = fields.Email()
    estado = fields.Str()

# Schema para Serie
class SerieSchema(Schema):
    id = fields.Int(dump_only=True)
    comprobante = fields.Str(required=True)
    serie = fields.Str(required=True)
    numero = fields.Int(required=True)

# Schema para Linea
class LineaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    estado = fields.Str()

# Schema para Clase
class ClaseSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    estado = fields.Str()

# Schema para Tienda
class TiendaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    empresa = fields.Str(required=True)

from marshmallow import Schema, fields

class VentaSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha = fields.Date(required=True)
    tipo_movimiento = fields.Str(required=True)
    tipo_venta = fields.Str(required=True)
    numero_comprobante = fields.Str(required=True)
    cliente = fields.Str(required=True)
    valor_venta = fields.Float(required=True)
    igv = fields.Float(required=True)
    total = fields.Float(required=True)
    estado = fields.Str(default="PROCESADA")

from marshmallow import Schema, fields

class CompraSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha = fields.Date(required=True)
    tipo_movimiento = fields.Str(required=True)
    tipo_compra = fields.Str(required=True)
    numero_documento = fields.Str(required=True)
    ruc_proveedor = fields.Str(required=True)
    subtotal = fields.Float(required=True)
    igv = fields.Float(required=True)
    total = fields.Float(required=True)
    estado = fields.Str(default="PROCESADA")
