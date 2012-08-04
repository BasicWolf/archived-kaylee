# This file is meant to be compiled as a part of kaylee.coffee

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
            data = ''
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
    _success = (data) ->
        if data.error? then error(data.error) else success(data)
    kl.ajax(url, 'POST', data, _success, error)
    return null

kl.get = (url, success, error) ->
    _success = (data) ->
        if data.error? then error(data.error) else success(data)
    kl.ajax(url, 'GET', null, success, error)
    return null
