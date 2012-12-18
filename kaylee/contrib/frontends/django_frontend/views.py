from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from kaylee import kl

def register_node(request):
    reg_data = kl.register(request.META['REMOTE_ADDR'])
    return json_response(reg_data)

#pylint: disable-msg=W0613
#W0613:  Unused argument 'request'
@csrf_exempt
@require_http_methods(["POST"])
def subscribe_node(request, app_name, node_id):
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)

@csrf_exempt
def actions(request, node_id):
    if request.method == 'GET':
        return json_response( kl.get_action(node_id) )
    elif request.method == 'POST':
        next_task = kl.accept_result(node_id, request.raw_post_data)
        return json_response(next_task)

def json_response(s):
    return HttpResponse(s, content_type = 'application/json')
