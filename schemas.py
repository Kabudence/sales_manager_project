from marshmallow import Schema, fields

# Schema para User
class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)


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

    idemp = fields.Str(required=True)  # Empresa relacionada
    periodo = fields.Str(required=True)  # Periodo
    idprod = fields.Str(required=True)  # ID del producto
    nomproducto = fields.Str(required=True)  # Nombre del producto
    umedida = fields.Str(required=True)  # Unidad de medida
    st_ini = fields.Int()  # Stock inicial
    st_act = fields.Int()  # Stock actual
    st_min = fields.Int()  # Stock mínimo
    pr_costo = fields.Float(required=True)  # Precio de costo
    modelo = fields.Str()  # Modelo del producto
    medida = fields.Str()  # Medida del producto
    estado = fields.Str()  # Estado del producto
    prventa = fields.Float(required=True)  # Precio de venta


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
    idlinea = fields.Int(required=True)
    nombre = fields.Str(required=True)
    idemp = fields.Int(required=True)
    estado = fields.Str(required=True)


# Schema para Clase
class ClaseSchema(Schema):
    id = fields.Int(dump_only=True)
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
    igv = fields.Float(required=True)
    total = fields.Float(required=True)
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
