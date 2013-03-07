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
        when "GET"
            if data?
                dl = []
                for key, val of data
                    dl.push(key + '=' + encodeURIComponent(val))
                url += '?' + dl.join('&')
            req.open("GET", url, true);

    req.onreadystatechange = () ->
        if req.readyState == 4
            if req.status == 200 and req.responseText?
                response = JSON.parse(req.responseText);
                if response.error?
                    fail(response.error)
                else
                    success(response)
            else if !response?
                fail('INVALID_STATE_ERR')
            else
                fail(response)
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


_dom_include = (urls, success, fail) ->
    if not (urls instanceof Array)
        urls = [urls]   # in this case string is expected
    count = urls.length
    sc = 0              # loaded scripts and stylesheets counter
    failed = false      # indicates whether the inclusion process failed or not

    for url in urls
        doc = document.getElementsByTagName('head')[0]

        onload = () ->
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
            js.onload = onload
            js.onerror = onerror
            doc.appendChild(js)
        else if util.ends_with(url, '.css')
            if fail?
                kl.exception('Kaylee is not able to invoke the fail()
                    callback of kl.include(..) when loading stylesheets.')
                failed = true
                return
            css = document.createElement("link")
            css.rel = 'stylesheet'
            css.type = 'text/css'
            css.href = url
            css.onload = onload
            doc.appendChild(css)
    return


_worker_include = (urls, success, fail) ->
    if not (urls instanceof Array)
        urls = [urls]   # in this case string is expected

    all_imported = true
    for url in urls
        try
            importScripts(url)
        catch error
            all_imported = false
            break

    if all_imported
        success?()
    else
        fail?(error)

kl.include = (urls, success, fail) ->
    # bind appropriate include function as kl.include
    if __DEFINE_WORKER?
        _worker_include(urls, success, fail)
    else
        _dom_include(urls, success, fail)
