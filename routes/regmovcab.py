from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import RegMovCab, RegMovDet, Producto
from schemas import RegMovCabSchema
from extensions import db
from services.notificacion_service import crear_notificacion
from services.products_service import search_product

regmovcab_bp = Blueprint('regmovcab_bp', __name__)
regmovcab_schema = RegMovCabSchema()
regmovcabs_schema = RegMovCabSchema(many=True)


# GET: Obtener todos los registros
@regmovcab_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_regmovcabs():
    regmovcabs = RegMovCab.query.all()
    return jsonify(regmovcabs_schema.dump(regmovcabs)), 200


# GET: Obtener un registro por ID
@regmovcab_bp.route('/<int:id>', methods=['GET'])
# @jwt_required()
def get_regmovcab(id):
    regmovcab = RegMovCab.query.get_or_404(id)
    return jsonify(regmovcab_schema.dump(regmovcab)), 200


# POST: Crear un nuevo registro
@regmovcab_bp.route('/', methods=['POST'])
@jwt_required()
def create_regmovcab():
    data = request.get_json()

    # Validar datos de entrada
    errors = regmovcab_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Crear el nuevo registro
    regmovcab = RegMovCab(**data)
    db.session.add(regmovcab)
    db.session.commit()
    return jsonify(regmovcab_schema.dump(regmovcab)), 201


# PUT: Actualizar un registro existente
@regmovcab_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_regmovcab(id):
    regmovcab = RegMovCab.query.get_or_404(id)
    data = request.get_json()

    # Validar datos de entrada
    errors = regmovcab_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Actualizar los campos del registro
    for key, value in data.items():
        setattr(regmovcab, key, value)

    db.session.commit()
    return jsonify(regmovcab_schema.dump(regmovcab)), 200


# DELETE: Eliminar un registro
@regmovcab_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_regmovcab(id):
    regmovcab = RegMovCab.query.get_or_404(id)
    db.session.delete(regmovcab)
    db.session.commit()
    return jsonify({"message": "Registro eliminado exitosamente"}), 200



# GET: Obtener un registro por num_docum
@regmovcab_bp.route('/search/<string:num_docum>', methods=['GET'])
@jwt_required()
def find_by_num_docum(num_docum):
    # Buscar el registro por num_docum
    regmovcab = RegMovCab.query.filter_by(num_docum=num_docum).first()

    if not regmovcab:
        return jsonify({"message": f"No se encontró un registro con num_docum: {num_docum}"}), 404

    return jsonify(regmovcab_schema.dump(regmovcab)), 200




#ESTE ES EL PUT PARA ASIGNAR LA BOLETA COMO COMPLETADO Y RELLENAR EL EMPLEADO.
# ASI QUE SOLO TIENES QUE PASARLE EL PARAMETRO DE EMPLEADO DNI
@regmovcab_bp.route('/change-state-to-complete/<int:idmov>', methods=['PUT'])
@jwt_required()
def change_state_to_complete(idmov):
    try:
        print(f"[DEBUG] Entrando a change_state_to_complete => idmov={idmov}")  # LOG

        # Buscar el registro correspondiente por idmov
        regmovcab = RegMovCab.query.get(idmov)
        if not regmovcab:
            print(f"[DEBUG] No existe regmovcab con idmov={idmov}, devolviendo 404")
            return jsonify({"message": f"No se encontró un registro con idmov: {idmov}"}), 404

        # Obtener los datos del body
        data = request.get_json()
        print(f"[DEBUG] Body recibido en JSON => {data}")  # LOG
        vendedor = data.get("vendedor")

        if not vendedor:
            print(f"[DEBUG] 'vendedor' no fue provisto en el JSON. Devolviendo 400")  # LOG
            return jsonify({"error": "El campo 'vendedor' es obligatorio"}), 400

        print(f"[DEBUG] Recibo vendedor={vendedor} => Actualizando estado y vendedor...")

        # Obtener el numdocum_regmovcab
        numdocum_regmovcab = regmovcab.num_docum  # Suponiendo que el campo numdocum está en RegMovCab

        # Actualizar el estado y el vendedor
        regmovcab.estado = 1
        regmovcab.vendedor = vendedor

        # Buscar los registros de regmovdet asociados al idmov
        regmovdets = RegMovDet.query.filter_by(idcab=idmov).all()
        print(f"[DEBUG] regmovdets encontrados: {len(regmovdets)}")  # LOG

        if not regmovdets:
            print(f"[DEBUG] No se encontraron productos asociados al idmov={idmov}")
            return jsonify({"message": f"No se encontraron productos asociados al registro con idmov: {idmov}"}), 404

        # Listas para almacenar detalles de las notificaciones
        detalles_notificacion = []
        alertas_stock_minimo = []
        alertas_stock_insuficiente = []

        # Actualizar las cantidades de los productos
        for regmovdet in regmovdets:
            print(f"[DEBUG] Procesando regmovdet.iddet={regmovdet.iddet}, producto={regmovdet.producto}, cantidad={regmovdet.cantidad}")  # LOG
            producto = Producto.query.filter_by(idprod=regmovdet.producto).first()

            if producto:
                print(f"[DEBUG] Producto encontrado => nomproducto={producto.nomproducto}, st_act={producto.st_act}")  # LOG

                if producto.st_act is not None:
                    nuevo_stock = producto.st_act - regmovdet.cantidad
                    if nuevo_stock < 0:
                        alerta_insuficiente = f"ALERTA: Stock insuficiente para el producto {producto.nomproducto}. Venta asociada a {numdocum_regmovcab}."
                        alertas_stock_insuficiente.append(alerta_insuficiente)
                    else:
                        print(f"[DEBUG] {producto.nomproducto} stock actualizado => st_act={nuevo_stock}")  # LOG
                        producto.st_act = nuevo_stock
                        detalles_notificacion.append(
                            f"{producto.nomproducto}: -{regmovdet.cantidad} unidades, Stock actual: {nuevo_stock}"
                        )

                        # Verificar si el stock actual alcanza el stock mínimo
                        if nuevo_stock == producto.st_min:
                            alerta = f"ALERTA: El producto {producto.nomproducto} alcanzó el stock mínimo ({producto.st_min}). Venta asociada a {numdocum_regmovcab}."
                            alertas_stock_minimo.append(alerta)

                else:
                    print(f"[DEBUG] {producto.nomproducto} no tiene st_act definido. Devolviendo 400")  # LOG
                    return jsonify(
                        {"error": f"El producto {producto.nomproducto} no tiene stock inicial definido"}), 400
            else:
                print(f"[DEBUG] No se encontró el producto con ID: {regmovdet.producto}, devolviendo 404")  # LOG
                return jsonify({"error": f"No se encontró el producto con ID: {regmovdet.producto}"}), 404

        # Confirmar cambios en la base de datos
        db.session.commit()
        print("[DEBUG] Cambio de estado y vendedor completado correctamente.")  # LOG

        # 📢 Crear notificación con los productos modificados
        if detalles_notificacion:
            mensaje_notificacion = f"Venta completada por {vendedor}. Productos modificados:\n" + "\n".join(detalles_notificacion)
            crear_notificacion(mensaje_notificacion, numdocum_regmovcab=numdocum_regmovcab)

        # 📢 Crear notificaciones de alerta por stock mínimo
        if alertas_stock_minimo:
            for alerta in alertas_stock_minimo:
                crear_notificacion(alerta, numdocum_regmovcab=numdocum_regmovcab)

        # 📢 Crear notificaciones de alerta por stock insuficiente
        if alertas_stock_insuficiente:
            for alerta_insuficiente in alertas_stock_insuficiente:
                crear_notificacion(alerta_insuficiente, numdocum_regmovcab=numdocum_regmovcab)

        return jsonify({
            "message": f"Estado del registro con idmov {idmov} actualizado a '1', vendedor modificado y productos actualizados con éxito",
            "updated_record": regmovcab_schema.dump(regmovcab)
        }), 200

    except Exception as e:
        print("[ERROR] Excepción en change_state_to_complete:")
        import traceback
        traceback.print_exc()  # LOG
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ESTE POST ES PARA CREAR LA BOLETA CON DATOS INCOMPLETOS
# SOLO REQUIERE ESTOS PARAMETOS:
# "tip_mov": "1",
# "tip_docum": "01",
# "num_docum": "F001-000123",
# "ruc_cliente": "10412942987",
# "vvta": "1269.07",
# "igv": "228.43",
# "total": "1497.50"
@regmovcab_bp.route('/create-inprocess', methods=['POST'])
@jwt_required()
def create_inprocess():
    try:
        data = request.get_json()

        # 📌 Extraer parámetros obligatorios
        tip_mov = data.get("tip_mov")
        tip_docum = data.get("tip_docum")
        num_docum = data.get("num_docum")
        ruc_cliente = data.get("ruc_cliente")
        vvta = data.get("vvta")
        igv = data.get("igv")
        total = data.get("total")
        item_list = data.get("ItemList")  # 🔹 Lista de productos

        # 📌 Validaciones
        if not all([tip_mov, tip_docum, num_docum, ruc_cliente, vvta, igv, total, item_list]):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # 📌 Fecha actual
        fecha_actual = datetime.now().date()

        # 📌 Crear nuevo registro en `regmovcab`
        nuevo_registro = RegMovCab(
            fecha=fecha_actual,
            tip_mov=int(tip_mov),
            tip_vta="01",
            tip_docum=tip_docum,
            num_docum=num_docum,
            ruc_cliente=ruc_cliente,
            vendedor=None,
            vvta=float(vvta),
            igv=float(igv),
            total=float(total),
            idemp="01",
            estado=2
        )

        db.session.add(nuevo_registro)
        db.session.flush()  # 🔹 Obtener `idmov` antes del commit

        idmov = nuevo_registro.idmov  # 🔹 ID de la cabecera creada

        # 📌 Procesar `ItemList` para `regmovdet`
        regmovdet_list = []
        for item in item_list:
            item_name = item.get("ItemName")
            item_quantity = float(item.get("ItemQuantity", 0))
            item_price = float(item.get("ItemPrice", 0))

            # 📌 Buscar el producto en la base de datos
            product = search_product(item_name, item_price)
            if not product:
                return jsonify({"error": f"Producto no encontrado: {item_name}"}), 400

            # 📌 Calcular valores
            product_id = product["idprod"]
            igv_calc = (item_price * 0.18)
            precio_calc = item_price * 0.82

            # 📌 Crear objeto `regmovdet`
            regmovdet = RegMovDet(
                idcab=idmov,
                producto=product_id,
                cantidad=item_quantity,
                precio=precio_calc,
                igv=igv_calc,
                total=item_price,
                st_act=1
            )

            regmovdet_list.append(regmovdet)

        # 📌 Guardar los detalles en la base de datos
        db.session.add_all(regmovdet_list)
        db.session.commit()

        return jsonify({
            "message": "Registro creado con éxito",
            "idmov": idmov,
            "regmovcab": regmovcab_schema.dump(nuevo_registro),
            "regmovdet": [{"producto": d.producto, "cantidad": d.cantidad, "precio": d.precio} for d in regmovdet_list]
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@regmovcab_bp.route('/create-compra', methods=['POST'])
@jwt_required()
def create_compra():
    """
    Crea un registro de COMPRA en RegMovCab (tip_mov = 2) sin solicitar la fecha, vvta, igv ni total.
    La fecha se obtiene como la fecha actual (hora local de Perú) y los valores se calculan a partir de los detalles:
      - vvta se calcula como la suma de (precio * cantidad) de cada ítem.
      - igv se calcula como la suma de (igv * cantidad) de cada ítem.
      - total se calcula como la suma de (precio + igv) * cantidad.
    Se actualiza el stock de cada producto sumando la cantidad comprada, buscando el producto según su código,
    y se genera una notificación normal con el detalle de los productos actualizados.

    Además, si se incluye en el JSON la información del proveedor (en el objeto "proveedor"),
    se crea una instancia en la tabla Proveedor usando:
      - Se solicitan: ruc, nomproveedor, direccion, contacto
      - Se completan: telefono="111111", celular="111111", correo="correo", estado=1
    """
    try:
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({"error": "No se recibió ningún cuerpo JSON"}), 400

        # 1. Extraer campos básicos para la compra
        num_docum = data.get("num_docum")
        ruc_cliente = data.get("ruc_cliente")
        item_list = data.get("ItemList")

        # Validar que existan los campos obligatorios para la compra
        if not all([num_docum, ruc_cliente, item_list]):
            return jsonify({"error": "Faltan datos obligatorios para la compra"}), 400

        # 2. Determinar tip_docum a partir de los primeros 4 caracteres de num_docum
        doc_prefix = num_docum[:4] if len(num_docum) >= 4 else ""
        if doc_prefix == "F001":
            tip_docum = "01"
        elif doc_prefix == "B001":
            tip_docum = "02"
        else:
            tip_docum = "00"  # Ajusta según la lógica de tu negocio

        # 3. Obtener la fecha actual (hora local de Perú)
        fecha_actual = datetime.now().date()

        # Inicializar acumuladores para calcular vvta, igv y total de la compra
        total_vvta = 0.0
        total_igv = 0.0
        total_total = 0.0

        regmovdet_list = []
        detalles_notificacion = []  # Acumulará los detalles para la notificación normal

        # 4. Procesar cada ítem en ItemList, calcular totales y actualizar el stock
        for item in item_list:
            # Extraer datos de cada ítem
            producto_id = item.get("producto")  # Código del producto
            cantidad = item.get("cantidad")
            precio = item.get("precio")
            igv_item = item.get("igv")

            # Validar campos obligatorios del ítem
            if not all([producto_id, cantidad, precio, igv_item]):
                return jsonify({"error": "Faltan datos (producto/cantidad/precio/igv) en algún ítem"}), 400

            cantidad = float(cantidad)
            precio = float(precio)
            igv_item = float(igv_item)
            # Calcular total para el ítem: (precio + igv) * cantidad
            total_item = (precio + igv_item) * cantidad

            # Acumular valores para la cabecera
            total_vvta += precio * cantidad
            total_igv += igv_item * cantidad
            total_total += total_item

            # Crear el registro de detalle (RegMovDet)
            regmovdet = RegMovDet(
                idcab=None,  # Se asignará luego al obtener el idmov
                producto=producto_id,
                cantidad=cantidad,
                precio=precio,
                igv=igv_item,
                total=total_item,
                st_act=1
            )
            regmovdet_list.append(regmovdet)

            # Actualizar el stock del producto: buscar por código y sumar la cantidad comprada
            producto_obj = Producto.query.filter_by(idprod=producto_id).first()
            if not producto_obj:
                return jsonify({"error": f"No se encontró el producto con ID {producto_id}"}), 404

            if producto_obj.st_act is None:
                return jsonify({"error": f"El producto {producto_obj.nomproducto} no tiene stock inicial definido"}), 400

            nuevo_stock = float(producto_obj.st_act) + cantidad
            producto_obj.st_act = nuevo_stock

            detalles_notificacion.append(
                f"{producto_obj.nomproducto}: +{cantidad} unidades, Nuevo stock: {nuevo_stock}"
            )

        # 5. Crear el registro en regmovcab usando los acumuladores calculados
        nuevo_regmovcab = RegMovCab(
            fecha=fecha_actual,
            tip_mov=2,         # 2 => COMPRA
            tip_vta="01",      # Ajusta si es necesario
            tip_docum=tip_docum,
            num_docum=num_docum,
            ruc_cliente=ruc_cliente,
            vendedor=None,
            vvta=total_vvta,
            igv=total_igv,
            total=total_total,
            idemp="01",
            estado=1           # estado=1 indica que la compra se completó
        )
        db.session.add(nuevo_regmovcab)
        db.session.flush()  # Permite obtener el idmov generado
        idmov = nuevo_regmovcab.idmov

        # Asignar el idmov a cada detalle
        for regmovdet in regmovdet_list:
            regmovdet.idcab = idmov

        # 6. Procesar la creación del proveedor (si se incluyen los datos en el JSON)
        proveedor_data = data.get("proveedor")
        if proveedor_data:
            ruc_prov = proveedor_data.get("ruc")
            nomproveedor = proveedor_data.get("nomproveedor")
            direccion_prov = proveedor_data.get("direccion")
            contacto_prov = proveedor_data.get("contacto")
            if not all([ruc_prov, nomproveedor, direccion_prov, contacto_prov]):
                return jsonify({"error": "Faltan datos obligatorios para el proveedor"}), 400

            # Importar o usar el modelo Proveedor (asegúrate de que esté definido en models)
            from models import Proveedor
            # Verificar si ya existe un proveedor con ese RUC
            proveedor_existente = Proveedor.query.get(ruc_prov)
            if not proveedor_existente:
                nuevo_proveedor = Proveedor(
                    ruc=ruc_prov,
                    nomproveedor=nomproveedor,
                    direccion=direccion_prov,
                    telefono="111111",
                    celular="111111",
                    contacto=contacto_prov,
                    correo="correo",
                    estado=1
                )
                db.session.add(nuevo_proveedor)

        # 7. Guardar los detalles de la compra y confirmar los cambios en la DB
        db.session.add_all(regmovdet_list)
        db.session.commit()

        # 8. Crear una notificación normal con el detalle de los productos actualizados
        if detalles_notificacion:
            msj_notificacion = (
                "Compra registrada. Productos actualizados:\n" +
                "\n".join(detalles_notificacion)
            )
            crear_notificacion(msj_notificacion, numdocum_regmovcab=num_docum)

        return jsonify({
            "message": "Compra registrada con éxito",
            "idmov": idmov,
            "regmovcab": regmovcab_schema.dump(nuevo_regmovcab),
            "regmovdet": [
                {
                    "producto": d.producto,
                    "cantidad": d.cantidad,
                    "precio": d.precio,
                    "igv": d.igv,
                    "total": d.total
                }
                for d in regmovdet_list
            ]
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500





