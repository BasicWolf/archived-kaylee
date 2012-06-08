# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request, Response

from kaylee import kl, load, settings

kaylee_blueprint = Blueprint('kaylee_blueprint', __name__,
                          template_folder = settings.FRONTEND_TEMPLATES_DIR)
klb = kaylee_blueprint

@klb.route('/register')
def register_node():
    reg_data = kl.register(request.remote_addr)
    return json_response(reg_data)

@klb.route('/apps/<app_name>/subscribe/<node_id>', methods = ['POST'])
def subscribe_node(node_id, app_name):
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)

@klb.route('/tasks/<node_id>', methods = ['GET', 'POST'])
def tasks(node_id):
    if request.method == 'GET':
        return json_response( kl.get_task(node_id) )
    else:
        next_task = kl.accept_result(node_id, request.json)
        return json_response(next_task)

def json_response(s):
    return Response(s, mimetype = 'application/json')
