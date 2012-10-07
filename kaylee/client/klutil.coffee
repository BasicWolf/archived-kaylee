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

kl = {}
kl.util = {}
util = kl.util

util.is_function = (obj) ->
    return typeof(obj) == 'function'


class Event
    constructor : (handler = null) ->
        @handlers = []
        @handlers.push(handler) if handler?
        return null

    trigger : (args...) =>
        for c in @handlers
            c(args...)
        return null

    bind : (handler) =>
        @handlers.push(handler)
        return null

    unbind : (handler) =>
        @handlers[t..t] = [] if (t = @handlers.indexOf(handler)) > -1
        return null
kl.Event = Event
