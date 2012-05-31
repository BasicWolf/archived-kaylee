# -*- coding: utf-8 -*-
import os
import imp

from flask import Flask, session, request, jsonify, render_template, json
from werkzeug import SharedDataMiddleware
from jinja2 import FileSystemLoader

# load Kaylee
import kaylee

settings = imp.load_source('settings', os.environ['KAYLEE_SETTINGS_PATH'])
kl = kaylee.load(settings)

app = Flask('kaylee')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/kaylee/register')
def register_node():
    reg_data = kl.register(request.remote_addr)
    return json_response(reg_data)

@app.route('/kaylee/apps/<app_name>/subscribe/<node_id>')
def subscribe_node(node_id, app_name):
    node_config = kl.subscribe(node_id, app_name)
    return json_response(node_config)

@app.route('/kaylee/tasks/<node_id>', methods = ['GET', 'POST'])
def tasks(node_id):
    if request.method == 'GET':
        return json_response( kl.get_task(node_id) )
    else:
        next_task = kl.accept_result(node_id, request.json)
        return json_response(next_task)

def json_response(s):
    return app.response_class(s, mimetype='application/json')

def run():
    STATIC_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/static'
    TEMPLATE_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/templates'
    app.jinja_loader = FileSystemLoader(TEMPLATE_DIR)
    app.static_path = STATIC_DIR
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                        { '/static': app.static_path } )
    app.debug = True
    app.run()
