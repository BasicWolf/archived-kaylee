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
    # The session code is used for performance and security:
    # * 'node_id' value from session will be compared to 'node_id'  extracted
    #   from the URL.
    # * If user refreshes the page, the same task could be given
    #   to the node again.
    if 'node_id' in session:
        _node_id = session.pop('node_id')
        try:
            node_id = NodeID(_node_id)
            # todo: dispatcher can give the same task again
            # e.g. dispatcher.renew(node_id)
            dispatcher.unregister(node_id)
        except InvalidNodeIDError:
            pass
    node_id = str( dispatcher.register(request.remote_addr) )
    session['node_id'] = node_id
    return jsonify(node_id = node_id,
                   applications = applications.names
                   )

@app.route('/kaylee/apps/<app_name>/subscribe/<node_id>')
def subscribe_node(node_id, app_name):
    node_config = dispatcher.subscribe(node_id, app_name)
    return json.dumps(node_config)


@app.route('/kaylee/tasks/<node_id>')
def tasks(node_id):
    data = dispatcher.get_task(node_id)
    return json.dumps(data)


def run():
    app.secret_key = "?9U'4IKHyT;)k~w7#Q+ag|N\n0iT~21"
    app.jinja_loader = FileSystemLoader(settings.FRONTEND_TEMPLATE_DIR)
    app.static_path = settings.FRONTEND_STATIC_DIR
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                        { '/static': app.static_path } )
    app.debug = True
    app.run()
