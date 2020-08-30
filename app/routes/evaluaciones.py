from flask import Blueprint, jsonify, request, abort, g
from ..models import Evaluacion
from ..controller import get_all_evaluaciones, get_evaluacion_by_id, insert_evaluacion, delete_evaluacion, update_evaluacion
from ..middleware import is_auth

evaluaciones_blueprint = Blueprint('evaluaciones_blueprint', __name__)

@evaluaciones_blueprint.route('/', methods=['GET'])
@is_auth
def get_evaluaciones():
    return jsonify(get_all_evaluaciones())

@evaluaciones_blueprint.route('/<int:id>', methods=['GET'])
@is_auth
def get_evaluacion(id):
    evaluacion = get_evaluacion_by_id(id)
    if evaluacion is None:
        abort(404)
    return evaluacion

@evaluaciones_blueprint.route('/', methods=['POST'])
@is_auth
def post_evaluacion():
    evaluacion = request.get_json()
    try:
        Evaluacion().load(evaluacion)
    except:
        abort(400)
    return insert_evaluacion(evaluacion)

@evaluaciones_blueprint.route('/<int:id>', methods=['PUT'])
@is_auth
def put_evaluacion(id):
    evaluacion = get_evaluacion_by_id(id)
    if evaluacion is None:
        abort(404)
    data = request.get_json()
    try:
        Evaluacion().load(data)
    except Exception:
        abort(400)
    evaluacion.update(data)
    return update_evaluacion(evaluacion, id)

@evaluaciones_blueprint.route('/<int:id>', methods=['DELETE'])
@is_auth
def remove_evaluacion(id):
    return delete_evaluacion(id)