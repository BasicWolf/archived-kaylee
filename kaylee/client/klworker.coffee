###
#    klworker.coffee
#    ~~~~~~~~~~~~~~~
#
#    This is the base file of Kaylee client-side Web Worker module.
#    This module is used to execute the AUTO-mode projects.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

kl = {}  # 'partial' kl namespace
klw = {} # Kaylee worker namespace
pj = {}  # Local project namespace

addEventListener('message', ((e) ->
    msg = e.data.msg
    mdata = e.data.data
    switch msg
        when 'import_project' then klw.import_project(mdata)
        when 'solve_task' then pj.solve(mdata)

    ), false
)

klw.post_message = (msg, data = {}) ->
    postMessage({'msg' : msg, 'data' : data})

klw.import_project = (kwargs) ->
    importScripts(kwargs.app_config.__kl_project_script__)
    pj.init(kwargs.kl_config, kwargs.app_config,
            (data) -> klw.post_error('__klw_error__', data)
    )

klw.task_completed = (res) ->
    klw.post_message('task_completed', res)

klw.log = (message) ->
    klw.post_message('__klw_log__', message)


# Kaylee project_imported event object simulation
kl.project_imported = {
    trigger = (data) ->
        klw.post_message('project_imported')
}

