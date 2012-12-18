# -*- coding: utf-8 -*-

from flask import Blueprint, request, Response
from kaylee import kl

bp = Blueprint('kaylee_blueprint', __name__)
kaylee_blueprint = bp # just an alias for importing convenience

@bp.route('/register')
def register_node():
    reg_data = kl.register(request.remote_addr)
    return json_response(reg_data)

@bp.route('/apps/<app_name>/subscribe/<node_id>', methods = ['POST'])
def subscribe_node(node_id, app_name):
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)

@bp.route('/actions/<node_id>', methods = ['GET', 'POST'])
def tasks(node_id):
    if request.method == 'GET':
        return json_response( kl.get_action(node_id) )
    else:
        next_task = kl.accept_result(node_id, request.data)
        # the reason for using request.data instead of request.json
        # is that Kaylee expects the "raw", non-processed data
        return json_response(next_task)

def json_response(s):
    return Response(s, mimetype = 'application/json')
