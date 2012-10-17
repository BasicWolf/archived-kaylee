###
#    klutil.coffee
#    ~~~~~~~~~~~~~
#
#    This is the base file of Kaylee client-side module.
#    It contains the common code used by Kaylee.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

util = {}
kl.util = util

util.is_function = (obj) ->
    return typeof(obj) == 'function'


class Event
    constructor : (handler = null) ->
        @handlers = []
        @handlers.push(handler) if handler?
        return

    trigger : (args...) =>
        for c in @handlers
            c(args...)
        return

    bind : (handler) =>
        @handlers.push(handler)
        return

    unbind : (handler) =>
        @handlers[t..t] = [] if (t = @handlers.indexOf(handler)) > -1
        return
kl.Event = Event
