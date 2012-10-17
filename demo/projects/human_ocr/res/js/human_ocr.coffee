pj = kl.pj

pj.init = (kl_config, app_config) ->
    pj._make_div()
    kl.project_imported.trigger()
    return

pj._make_div = () ->
    div = document.createElement('div');
    div.id = 'human_ocr';
    if document.body.firstChild
        document.body.insertBefore(div, document.body.firstChild);
    else
        document.body.appendChild(div);
    return

pj.on_task_received = (data) ->
    return
