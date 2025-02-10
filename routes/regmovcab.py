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
# @jwt_required()
def find_by_num_docum(num_docum):
    # Buscar el registro por num_docum
    regmovcab = RegMovCab.query.filter_by(num_docum=num_docum).first()

    if not regmovcab:
        return jsonify({"message": f"No se encontró un registro con num_docum: {num_docum}"}), 404

    return jsonify(regmovcab_schema.dump(regmovcab)), 200




#ESTE ES EL PUT PARA ASIGNAR LA BOLETA COMO COMPLETADO Y RELLENAR EL EMPLEADO.
# ASI QUE SOLO TIENES QUE PASARLE EL PARAMETRO DE EMPLEADO DNI
@regmovcab_bp.route('/change-state-to-complete/<int:idmov>', methods=['PUT'])
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
# @jwt_required()
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
            igv_calc = (item_price * 1.18) - item_price
            total_calc = item_price * 1.18

            # 📌 Crear objeto `regmovdet`
            regmovdet = RegMovDet(
                idcab=idmov,
                producto=product_id,
                cantidad=item_quantity,
                precio=item_price,
                igv=igv_calc,
                total=total_calc,
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