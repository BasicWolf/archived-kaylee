###
#    klutil.coffee
#    ~~~~~~~~~~~~~
#
#    This file is a part of Kaylee client-side module.
#    It contains the util and shared code used by Kaylee.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

kl.util = util = {}

util.is_function = (obj) ->
    return typeof(obj) == 'function'

util.ends_with = (str, suffix) ->
    return str.indexOf(suffix, str.length - suffix.length) != -1


kl.Event = class Event
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

# currently (01.12.2012) a hack, hopefully will be fixed in newer
# versions of CoffeeScript
kl.KayleeError = class KayleeError extends Error then constructor: -> super

util.after = (timeout, f) ->
    setTimeout(f, timeout)

util.every = (period, f) ->
    setInterval(f, period)