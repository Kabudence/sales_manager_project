from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import RegMovDet, Producto, RegMovCab
from schemas import RegMovDetSchema

# Crear el Blueprint para regmovdet
regmovdet_bp = Blueprint('regmovdet_bp', __name__)

# Crear los esquemas para serialización
regmovdet_schema = RegMovDetSchema()
regmovdets_schema = RegMovDetSchema(many=True)

# GET: Obtener todos los registros
@regmovdet_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_regmovdet():
    regmovdets = RegMovDet.query.all()
    return jsonify(regmovdets_schema.dump(regmovdets)), 200


# GET: Obtener un registro por iddet
@regmovdet_bp.route('/<int:iddet>', methods=['GET'])
@jwt_required()
def get_regmovdet(iddet):
    regmovdet = RegMovDet.query.get_or_404(iddet)
    return jsonify(regmovdet_schema.dump(regmovdet)), 200


# import logging  # (REMOVIDO)
# logging.basicConfig(level=logging.DEBUG)  # (REMOVIDO)
# logger = logging.getLogger(__name__)  # (REMOVIDO)

@regmovdet_bp.route('/by-idcab/<int:idcab>', methods=['GET'])
def get_regmovdet_by_idcab_join(idcab):
    try:
        # logger.info(f"Iniciando búsqueda de regmovdet con idcab = {idcab} (JOIN)")  # (REMOVIDO)

        resultados = db.session.query(RegMovDet, Producto.nomproducto).\
            join(Producto, RegMovDet.producto == Producto.idprod).\
            filter(RegMovDet.idcab == idcab).all()

        # logger.warning(f"No se encontraron registros para idcab {idcab} (JOIN)")  # (REMOVIDO)
        if not resultados:
            return jsonify({"message": f"No se encontraron registros para idcab {idcab}"}), 404

        # logger.info(f"Se encontraron {len(resultados)} registros para idcab {idcab} (JOIN)")  # (REMOVIDO)

        salida = []
        for regmovdet, nomproducto in resultados:
            # logger.debug(f"Procesando registro: iddet={regmovdet.iddet}, producto={regmovdet.producto}, nomproducto={nomproducto}")  # (REMOVIDO)
            salida.append({
                "iddet": regmovdet.iddet,
                "idcab": regmovdet.idcab,
                "producto": regmovdet.producto,
                "cantidad": float(regmovdet.cantidad),
                "precio": float(regmovdet.precio),
                "igv": float(regmovdet.igv),
                "total": float(regmovdet.total),
                "st_act": float(regmovdet.st_act),
                "nomproducto": nomproducto
            })

        # logger.info("Consulta con JOIN completada con éxito.")  # (REMOVIDO)
        return jsonify(salida), 200

    except Exception as e:
        # logger.error(f"Error en get_regmovdet_by_idcab_join: {e}", exc_info=True)  # (REMOVIDO)
        return jsonify({"error": str(e)}), 500


@regmovdet_bp.route('/by-num-doc/<string:num_docum>', methods=['GET'])
@jwt_required()
def get_regmovdet_by_num_doc_join(num_docum):
    try:
        # logger.info(f"Iniciando búsqueda de regmovdet con num_docum = {num_docum} (JOIN)")  # (REMOVIDO)

        # 1. Buscar la cabecera en regmovcab para obtener el idmov
        cabecera = RegMovCab.query.filter_by(num_docum=num_docum).first()

        # logger.warning(f"No se encontró cabecera con num_docum = {num_docum}")  # (REMOVIDO)
        if not cabecera:
            return jsonify({"message": f"No se encontró regmovcab con num_docum {num_docum}"}), 404

        idcab = cabecera.idmov

        # 2. Realizar la consulta JOIN en regmovdet filtrando por idcab
        resultados = db.session.query(RegMovDet, Producto.nomproducto).\
            join(Producto, RegMovDet.producto == Producto.idprod).\
            filter(RegMovDet.idcab == idcab).all()

        # logger.warning(f"No se encontraron detalles (regmovdet) para idcab {idcab}")  # (REMOVIDO)
        if not resultados:
            return jsonify({"message": f"No se encontraron registros para num_docum {num_docum}"}), 404

        # logger.info(f"Se encontraron {len(resultados)} registros para num_docum = {num_docum} (JOIN)")  # (REMOVIDO)

        salida = []
        for regmovdet, nomproducto in resultados:
            # logger.debug(f"Procesando registro: iddet={regmovdet.iddet}, producto={regmovdet.producto}, nomproducto={nomproducto}")  # (REMOVIDO)
            salida.append({
                "iddet": regmovdet.iddet,
                "idcab": regmovdet.idcab,
                "producto": regmovdet.producto,
                "cantidad": float(regmovdet.cantidad),
                "precio": float(regmovdet.precio),
                "igv": float(regmovdet.igv),
                "total": float(regmovdet.total),
                "st_act": float(regmovdet.st_act),
                "nomproducto": nomproducto
            })

        # logger.info("Consulta con JOIN completada con éxito.")  # (REMOVIDO)
        return jsonify(salida), 200

    except Exception as e:
        # logger.error(f"Error en get_regmovdet_by_num_doc_join: {e}", exc_info=True)  # (REMOVIDO)
        return jsonify({"error": str(e)}), 500


# POST: Crear un nuevo registro
@regmovdet_bp.route('/', methods=['POST'])
@jwt_required()
def create_regmovdet():
    data = request.get_json()

    # Validar los datos de entrada
    errors = regmovdet_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Crear el nuevo registro
    regmovdet = RegMovDet(**data)
    db.session.add(regmovdet)
    db.session.commit()
    return jsonify(regmovdet_schema.dump(regmovdet)), 201


# PUT: Actualizar un registro existente
@regmovdet_bp.route('/<int:iddet>', methods=['PUT'])
@jwt_required()
def update_regmovdet(iddet):
    regmovdet = RegMovDet.query.get_or_404(iddet)
    data = request.get_json()

    # Validar los datos de entrada
    errors = regmovdet_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Actualizar los campos del registro
    for key, value in data.items():
        setattr(regmovdet, key, value)

    db.session.commit()
    return jsonify(regmovdet_schema.dump(regmovdet)), 200


# DELETE: Eliminar un registro
@regmovdet_bp.route('/<int:iddet>', methods=['DELETE'])
@jwt_required()
def delete_regmovdet(iddet):
    regmovdet = RegMovDet.query.get_or_404(iddet)
    db.session.delete(regmovdet)
    db.session.commit()
    return jsonify({"message": "Registro eliminado exitosamente"}), 200
