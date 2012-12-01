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

util.ends_with = (str, suffix) ->
    return str.indexOf(suffix, str.length - suffix.length) != -1

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


# currently (01.12.2012) a hack, hopefully will be fixed in newer
# versions of CoffeeScript
class KayleeError extends Error then constructor: -> super

kl.KayleeError = KayleeError