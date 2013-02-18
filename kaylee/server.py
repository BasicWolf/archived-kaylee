# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging

from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

from kaylee.contrib.frontends.werkzeug_frontend import url_map


log = logging.getLogger(__name__)

@Request.application
def application(request):
    adapter = url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        endpoint(**values)
    except HTTPException as e:
        return e


def run(settings_file, static_dir):
    setup_logging()

    # setup Kaylee
    import kaylee
    kaylee.setup(settings_file)

    from werkzeug.serving import run_simple

    build_dir = get_build_dir()

    app = SharedDataMiddleware(application,
                               {'/static': static_dir })

    run_simple('127.0.0.1', 5000, application, use_debugger=True,
               use_reloader=True)


def get_build_dir():
    # TODO:
    # kl.settings == file!
    # settings_dir = os.path.dirname(settings_path)
    # return os.path.abspath(os.path.join(settings_dir, '_build/'))
    return '/'

def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()
