###
    klajax.coffee
    ~~~~~~~~~~~~~

    This is the base file of Kaylee client-side module.
    It contains a small AJAX library used in a browser's
    main JavaScript event loop.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
###

kl.ajax = (url, method, data, success = (()->), error = (() ->) ) ->
    req = new XMLHttpRequest();

    switch method
        when "POST"
            data = {} if not data?
            data = JSON.stringify(data)
            req.open('POST', url, true);
            req.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            req.setRequestHeader("Content-length", data.length);
            req.setRequestHeader("Connection", "close");
        when "GET"
            if data?
                alert data
                dl = []
                for key, val of data
                    dl.push(key + '=' + encodeURIComponent(val))
                url += '?' + dl.join('&')
            req.open("GET", url, true);
    req.responseType = 'json'

    req.onreadystatechange = () ->
        if req.readyState == 4
            if req.status == 200 and req.response?
                if req.response.error?
                    error(req.response.error)
                else
                    success(req.response)
            else if !req.response?
                error('INVALID_STATE_ERR')
            else
                error(req.response)
        return null

    req.send(data);
    return null

kl.post = (url, data, success, error) ->
    _success = (resp_data) ->
        if resp_data.error? then error(resp_data.error) else success(resp_data)
    kl.ajax(url, 'POST', data, _success, error)
    return null

kl.get = (url, data, success, error) ->
    # remap the arguments in case that the first argument is
    # the success callback.
    if arguments.length >= 2
        if kl.util.is_function(data)
            error = success
            success = data
            data = null

    _success = (resp_data) ->
        if resp_data.error? then error(resp_data.error) else success(resp_data)
    kl.ajax(url, 'GET', data, _success, error)
    return null
