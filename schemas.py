from marshmallow import Schema, fields

# Schema para User
class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)
    role = fields.Str(required=True)


class ClienteSchema(Schema):
    idcliente = fields.Str(required=True)
    tdoc = fields.Str(required=True)
    nomcliente = fields.Str(required=True)
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=True)
    estado = fields.Str(required=True)

# Schema para Proveedor
class ProveedorSchema(Schema):
    ruc = fields.Str(required=True)  # Campo obligatorio según tu base de datos
    nomproveedor = fields.Str(required=True)
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=True)
    celular = fields.Str()  # Campo opcional
    contacto = fields.Str()  # Campo opcional
    correo = fields.Email()  # Validamos que sea un email válido
    estado = fields.Str()

# Schema para Producto

class ProductoSchema(Schema):
    idemp = fields.Str(required=True)
    periodo = fields.Str(required=True)
    idprod = fields.Str(required=True)
    nomproducto = fields.Str(required=True)
    umedida = fields.Str(required=True)
    st_ini = fields.Int()
    st_act = fields.Int()
    st_min = fields.Int()
    pr_costo = fields.Float(required=True)
    modelo = fields.Str()
    medida = fields.Str()
    estado = fields.Int()  # Cambiado a Integer
    prventa = fields.Float(required=True)


class VendedorSchema(Schema):
    idvend = fields.Int(required=True)  # Ahora se permite enviar este campo
    nomvendedor = fields.Str(required=True)
    direccion = fields.Str()
    telefono = fields.Str()
    correo = fields.Email()
    idemp = fields.Int(required=True)
    estado = fields.Str(required=True)


class SerieSchema(Schema):
    tcomp = fields.Str(required=True)
    serie = fields.Str(required=True)
    numero = fields.Int(required=True)
    idemp = fields.Int(required=True)

# Schema para Linea
class LineaSchema(Schema):
    idlinea = fields.Int(dump_only=True)  # autoincrement, no se envía
    nombre = fields.Str(required=True)
    idemp = fields.Str(required=True)
    estado = fields.Str(required=True)


# Schema para Clase
class ClaseSchema(Schema):
    idclase = fields.Int(dump_only=True)  # Solo para serialización
    nombres = fields.Str(required=True)  # Campo obligatorio
    idemp = fields.Int(required=True)  # Campo obligatorio
    estado = fields.Str(required=True)

# Schema para Tienda
class TiendaSchema(Schema):
    idemp = fields.Str(required=True)
    nombree = fields.Str(required=True)




# class VentaSchema(Schema):
#     fecha = fields.Date(required=True)
#     tipo_movimiento = fields.Str(required=True)
#     tipo_venta = fields.Str(required=True)
#     num_docum = fields.Str(required=True)
#     ruc_cliente = fields.Str(required=True)
#     cliente = fields.Str(required=True)
#     valor_de_venta = fields.Float(required=True)
#     igv = fields.Float(required=True)
#     total = fields.Float(required=True)
#     estado = fields.Str(required=True)
#
#


class CompraSchema(Schema):
    fecha = fields.Date(required=True)
    tipo_movimiento = fields.Str(required=True)
    tipo_venta = fields.Str(required=True)
    num_docum = fields.Str(required=True)
    ruc_cliente = fields.Str(required=True)
    proveedor = fields.Str(required=True)
    valor_de_venta = fields.Float(required=True)
    igv = fields.Str(required=True)
    total = fields.Str(required=True)
    estado = fields.Str(required=True)



class RegMovCabSchema(Schema):
    idmov = fields.Int(dump_only=True)  # Primary Key
    fecha = fields.Date(required=True)
    tip_mov = fields.Int(required=True)
    tip_vta = fields.Int(required=True)
    tip_docum = fields.Str(required=True)
    num_docum = fields.Str(required=True)
    ruc_cliente = fields.Str(allow_none=True)  # Foreign Key, puede ser opcional
    vendedor = fields.Str(allow_none=True)
    vta = fields.Float(required=True)
    igv = fields.Float(required=True)
    total = fields.Float(required=True)
    idemp = fields.Str(required=True)  # Empresa relacionada
