pj = kl.pj

pj.init = (kl_config, app_config) ->
    pj._make_div()
    kl.include(app_config.styles, kl.project_imported.trigger)
    return

pj._make_div = () ->
    div = document.createElement('div');
    div.id = 'human_ocr';
    div.innerHTML = """
        <table>
            <tr>
                <td>
                    <div id="human_ocr_img_container"></div>
                </td>
            </tr>

            <tr>
                <td>
                    <input id="human_ocr_input" type="text">
                </td>
                <td>
                    <button id="human_ocr_btnSend" type="button">Send</button>
                </td>
            </tr>
        </table>
    """
    if document.body.firstChild
        document.body.insertBefore(div, document.body.firstChild);
    else
        document.body.appendChild(div);

    return

pj.on_task_received = (data) ->
    return
