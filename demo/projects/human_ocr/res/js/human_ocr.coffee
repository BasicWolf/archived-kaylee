pj = kl.pj

pj.init = (kl_config, app_config) ->
    pj._make_div()
    kl.project_imported.trigger()
    return

pj.process_task = (data) ->
    img =  document.getElementById('human_ocr_img');
    img.src = "#{data.url}";
    return

pj._send = () ->
    val = document.getElementById('human_ocr_input').value
    kl.task_completed.trigger({ 'captcha' : val })
    pj._clear_input()

pj._refresh = () ->
    kl.task_completed.trigger(kl.NO_RESULT)
    pj._clear_input()

pj._clear_input = () ->
    document.getElementById('human_ocr_input').value = ''

pj._make_div = () ->
    div = document.createElement('div');
    div.id = 'human_ocr';
    div.innerHTML = """
        <table id="human_ocr_table">
            <tr>
                <td colspan="2">
                    <div><img id="human_ocr_img"/></div>
                </td>
            </tr>

            <tr>
                <td>
                    <input id="human_ocr_input"
                           type="text"
                           onKeyPress="{if (event.keyCode==13) pj._send(); }">
                </td>
                <td>
                    <button id="human_ocr_send_button"
                            class="human_ocr_button"
                            onclick="pj._send();">
                        Send
                    </button>
                    <button id="human_ocr_refresh_button"
                            class="human_ocr_button"
                            onclick="pj._refresh();">
                        Refresh
                    </button>
                </td>
            </tr>
        </table>
    """
    if document.body.firstChild
        document.body.insertBefore(div, document.body.firstChild);
    else
        document.body.appendChild(div);

    return
