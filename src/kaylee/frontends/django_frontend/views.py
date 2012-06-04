from django.http import HttpResponse

import kaylee
kl = kaylee.load()

def register_node(request):
    reg_data = kl.register(request.META['REMOTE_ADDR'])
    return json_response(reg_data)

def subscribe_node(request, app_name, node_id):
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)


def tasks(request, node_id):
    if request.method == 'GET':
        return json_response( kl.get_task(node_id) )
    else:
        next_task = kl.accept_result(node_id, request.json)
        return json_response(next_task)

def json_response(s):
    return HttpResponse(s, content_type = 'application/json')
