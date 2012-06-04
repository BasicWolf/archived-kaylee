from flask import Flask, render_template
from jinja2 import FileSystemLoader
from werkzeug import SharedDataMiddleware

import kl_settings
from kaylee.frontends.kaylee_flask import kaylee_blueprint

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

def run():

    app.register_blueprint(kaylee_blueprint,
                           static_folder = kl_settings.FRONTEND_STATIC_DIR,
                           url_prefix = '/kaylee')

    app.jinja_loader = FileSystemLoader(kl_settings.FRONTEND_TEMPLATES_DIR)
    app.static_path = kl_settings.FRONTEND_STATIC_DIR
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                        { '/static': app.static_path } )
    app.debug = True
    app.run()
