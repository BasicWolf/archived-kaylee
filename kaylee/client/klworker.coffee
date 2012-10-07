###
#    klworker.coffee
#    ~~~~~~~~~~~~~~~
#
#    This is the base file of Kaylee client-side Web Worker module.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

klw = {} # Kaylee worker namespace
pj = {}  # Project namespace

addEventListener('message', ((e) ->
    msg = e.data.msg
    mdata = e.data.data
    switch msg
        when 'import_project' then klw.import_project(mdata)
        when 'solve_task' then pj.on_task_received(mdata)

    ), false
)

klw.post_message = (msg, data = {}) ->
    postMessage({'msg' : msg, 'data' : data})

klw.import_project = (kwargs) ->
    importScripts(kwargs.app_config.script)
    pj.init(kwargs.kl_config, kwargs.app_config)
    klw.post_message('project_imported')

klw.task_completed = (res) ->
    klw.post_message('task_completed', res)

klw.log = (message) ->
    klw.post_message('__klw_log__', message)