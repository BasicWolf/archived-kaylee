from flask import Flask, session, request, jsonify, render_template
from werkzeug import SharedDataMiddleware
from jinja2 import FileSystemLoader

from kaylee import settings, dispatcher, NodeID
from kaylee.errors import InvalidNodeIDError
from kaylee import applications

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
        _nid = session.pop('node_id')
        try:
            nid = NodeID(_nid)
            # todo: dispatcher can give the same task again
            # e.g. dispatcher.renew(nid)
            dispatcher.unregister(nid)
        except InvalidNodeIDError:
            pass
    nid = str( dispatcher.register(request.remote_addr) )
    session['node_id'] = nid
    apps = [app.name for app in applications]
    return jsonify(nid = nid,
                   applications = apps)

@app.route('/kaylee/apps/{app_name}/subscribe')
def subscribe_node(app_name):
    pass

def run():
    app.secret_key = "?9U'4IKHyT;)k~w7#Q+ag|N\n0iT~21"
    app.jinja_loader = FileSystemLoader(settings.FRONTEND_TEMPLATE_DIR)
    app.static_path = settings.FRONTEND_STATIC_DIR
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                        { '/static': app.static_path } )
    app.debug = True
    app.run()
