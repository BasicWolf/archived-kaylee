###
#    klajax.coffee
#    ~~~~~~~~~~~~~
#
#    This is the base file of Kaylee client-side module.
#    It contains a small AJAX library used in a browser's
#    main JavaScript event loop.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

kl.ajax = (url, method, data, success = (()->), fail = (() ->) ) ->
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
                    fail(req.response.error)
                else
                    success(req.response)
            else if !req.response?
                fail('INVALID_STATE_ERR')
            else
                fail(req.response)
        return

    req.send(data);
    return

kl.post = (url, data, success, fail) ->
    _success = (resp_data) ->
        if resp_data.error? then fail(resp_data.error) else success(resp_data)
    kl.ajax(url, 'POST', data, _success, fail)
    return

kl.get = (url, data, success, fail) ->
    # remap the arguments in case that the first argument is
    # the success callback.
    if arguments.length >= 2
        if kl.util.is_function(data)
            fail = success
            success = data
            data = null

    _success = (resp_data) ->
        if resp_data.error? then fail(resp_data.error) else success(resp_data)
    kl.ajax(url, 'GET', data, _success, fail)
    return


kl.include = (urls, success, fail) ->
    if not urls instanceof Array
        urls = [urls]   # in this case string is expected
    count = urls.length
    sc = 0              # loaded scripts ('*.js' files) counter
    failed = false

    for url in urls
        doc = document.getElementsByTagName('head')[0]

        onload = () ->
            console.log('loaded: ')
            console.log(@)
            sc += 1
            if sc == count and not failed
                success?()

        onerror = (msg) ->
            failed = true
            fail?(msg)

        if util.ends_with(url, '.js')
            js = document.createElement('script')
            js.setAttribute('type', 'text/javascript')
            js.setAttribute('src', url)
            doc.appendChild(js)
            js.onload = onload
            js.onerror = onerror
        else if util.ends_with(url, '.css')
            css = document.createElement("link")
            css.rel = 'stylesheet'
            css.type = 'text/css'
            css.href = url
            doc.appendChild(css)
            css.onload = onload
            count -= 1 # don't block no matter what the status of CSS is
    return