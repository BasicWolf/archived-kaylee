klw = {} # Kaylee worker namespace

addEventListener('message', ((e) ->
    msg = e.data.msg
    mdata = e.data.data
    switch msg
        when 'import_project' then klw.import_project(mdata)
        when 'solve_task' then pj.on_task_recieved(mdata)

    ), false
)

klw.post_message = (msg, data = {}) ->
    postMessage({'msg' : msg, 'data' : data})

klw.import_project = (data) ->
    importScripts(data.script)
    pj.init(data.config)
    klw.post_message('project_imported')

klw.task_completed = (res) ->
    klw.post_message('task_completed', res)
