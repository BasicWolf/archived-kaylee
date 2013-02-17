# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

from kaylee import kl

log = logging.getLogger(__name__)

def kaylee_register_node():
    reg_data = kl.register(request.remote_addr)
    return json_response(reg_data)

def kaylee_subscribe_node(app_name, node_id):
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)

def kaylee_process_task(node_id):
    if request.method == 'GET':
        return json_response(kl.get_action(node_id))
    else:
        next_task = kl.accept_result(node_id, request.data)
        # the reason for using request.data instead of request.json
        # is that Kaylee expects the "raw", non-processed data
        return json_response(next_task)


url_map = Map([
    Rule('/register',
         methods=['GET'],
         endpoint=kaylee_register_node),
    Rule('/apps/<app_name>/subscribe/<node_id>',
         methods=['POST'],
         endpoint=kaylee_subscribe_node),
    Rule('/actions/<node_id>',
         methods=['GET', 'POST'],
         endpoint=kaylee_process_task)
])

@Request.application
def application(request):
    adapter = url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        endpoint(**values)
    except HTTPException as e:
        return e


def json_response(s):
    return Response(s, mimetype = 'application/json')



def run(settings_path):
    setup_logging()
    setup_kaylee(settings_path)

    from werkzeug.serving import run_simple

    build_dir = get_build_dir(settings_path)

    app = SharedDataMiddleware(application,
                               {'/static': build_dir })

    run_simple('127.0.0.1', 5000, application, use_debugger=True,
               use_reloader=True)


def get_build_dir(settings_path):
    settings_dir = os.path.dirname(settings_path)
    return os.path.abspath(os.path.join(settings_dir, '_build/'))

def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


def setup_kaylee(settings_path):
    import kaylee
    kaylee.setup(settings_path)


if __name__ == '__main__':
    main()
