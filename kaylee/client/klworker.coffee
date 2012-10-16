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

# Note that this is a WORKER script. It has no access to global
# data, document or window objects.

klw = {} # Kaylee worker namespace
pj = {}  # Local project namespace


on_worker_event = (e) ->
    msg = e.data.msg
    mdata = e.data.data
    switch msg
        when 'import_project' then klw.import_project(mdata)
        when 'solve_task' then pj.solve(mdata)

addEventListener('message', on_worker_event, false)

klw.post_message = (msg, data = {}) ->
    postMessage({'msg' : msg, 'data' : data})

klw.import_project = (kwargs) ->
    importScripts(kwargs.app_config.__kl_project_script__)
    pj.init(kwargs.kl_config, kwargs.app_config,
            (data) -> klw.post_error('__klw_error__', data)
    )

klw.log = (message) ->
    klw.post_message('__klw_log__', message)


# Although the events and handlers  below look alike the code
# in kaylee.coffee note, that this code is mainly used to send
# the messages from current WORKER to the main JS loop in which
# Kaylee Client to Server communication is established.
#
# Mostly the code below is used to keep the kaylee.coffee and
# klworker.coffee interfaces a bit similar.
on_project_imported = () ->
    klw.post_message('project_imported')

on_task_completed = (result) ->
    klw.post_message('task_completed', result)

kl.project_imported = new Event(on_project_imported)
kl.task_completed = new Event(on_task_completed)
