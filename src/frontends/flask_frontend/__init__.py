# -*- coding: utf-8 -*-
from flask import Flask, session, request, jsonify, render_template, json
from werkzeug import SharedDataMiddleware
from jinja2 import FileSystemLoader

from kaylee import settings, applications, dispatcher, NodeID
from kaylee.errors import InvalidNodeIDError

app = Flask('kaylee')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/kaylee/register')
def register_node():
    reg_data = dispatcher.register(request.remote_addr)
    return json_response(reg_data)

@app.route('/kaylee/apps/<app_name>/subscribe/<node_id>')
def subscribe_node(node_id, app_name):
    node_config = dispatcher.subscribe(node_id, app_name)
    return json_response(node_config)

@app.route('/kaylee/tasks/<node_id>', methods = ['GET', 'POST'])
def tasks(node_id):
    if request.method == 'GET':
        return json_response( dispatcher.get_task(node_id) )
    else:
        next_task = dispatcher.accept_result(node_id, request.json)
        return json_response(next_task)

def json_response(s):
    return app.response_class(s, mimetype='application/json')

def run():
#    app.secret_key = "?9U'4IKHyT;)k~w7#Q+ag|N\n0iT~21"
    app.jinja_loader = FileSystemLoader(settings.FRONTEND_TEMPLATE_DIR)
    app.static_path = settings.FRONTEND_STATIC_DIR
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                        { '/static': app.static_path } )
    app.debug = True
    app.run()
