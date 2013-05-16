# -*- coding: utf-8 -*-

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response
from kaylee import kl

def kaylee_register_node(request):
    reg_data = kl.register(request.remote_addr)
    return json_response(reg_data)

def kaylee_subscribe_node(request, app_name, node_id):
    #pylint: disable-msg=W0613
    #W0613:  Unused argument 'request'
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)

def kaylee_process_task(request, node_id):
    if request.method == 'GET':
        return json_response(kl.get_action(node_id))
    else:
        next_task = kl.accept_result(node_id, request.data)
        # the reason for using request.data instead of request.json
        # is that Kaylee expects the "raw", non-processed data
        return json_response(next_task)

def json_response(s):
    return Response(s, mimetype = 'application/json')

def make_url_map(url_prefix='/kaylee'):
    return Map([
        Rule(url_prefix + '/register',
             methods=['GET'],
             endpoint=kaylee_register_node),
        Rule(url_prefix + '/apps/<app_name>/subscribe/<node_id>',
             methods=['POST'],
             endpoint=kaylee_subscribe_node),
        Rule(url_prefix + '/actions/<node_id>',
             methods=['GET', 'POST'],
             endpoint=kaylee_process_task)
    ])
