# -*- coding: utf-8 -*-
import os
import sys
import argparse

from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.routing import Rule
from werkzeug.serving import run_simple

import kaylee
from kaylee.contrib.frontends.werkzeug_frontend import url_map as urls

import logging
log = logging.getLogger(__name__)

@Request.application
def application(request):
    adapter = urls.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        return endpoint(**values)
    except HTTPException as e:
        return e


def run(settings_file, static_dir):
    setup_logging()
    kaylee.setup(settings_file)

    # index.html at 'http://server.address/' URL
    with open(os.path.join(static_dir, 'index.html')) as f:
        index_data = f.read()
    def _home():
        return Response(index_data, mimetype='text/html')
    home_rule = Rule('/', methods=['GET'], endpoint=_home)
    urls.add(home_rule)

    log.debug(static_dir)
    # add static data middleware and start the server
    app = SharedDataMiddleware(application,
                               {'/static': static_dir })
    run_simple('127.0.0.1', 5000, app, use_debugger=True,
               use_reloader=True)


def setup_logging():
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    main()
