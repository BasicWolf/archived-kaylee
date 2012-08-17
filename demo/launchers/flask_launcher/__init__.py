from flask import Flask, render_template
from jinja2 import FileSystemLoader
from werkzeug import SharedDataMiddleware

from kaylee.contrib.frontends.flask_frontend import kaylee_blueprint

import kaylee_demo

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

def run():
    app.register_blueprint(kaylee_blueprint,
                           static_folder = kaylee_demo.FRONTEND_STATIC_DIR,
                           url_prefix = '/kaylee')

    app.jinja_loader = FileSystemLoader(kaylee_demo.FRONTEND_TEMPLATES_DIR)
    app.static_path = kaylee_demo.FRONTEND_STATIC_DIR
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                        { '/static': app.static_path } )
    app.debug = True
    app.run()
