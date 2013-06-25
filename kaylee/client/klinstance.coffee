###
#    klinstance.coffee
#    ~~~~~~~~~~~~~~~~~~
#
#    This file is a part of Kaylee client-side module.
#    It contains routines which help running only one
#    instance of Kaylee per host per browser.
#
#    :copyright: (c) 2013 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###
kl.instance = instance = {}

PING = "kaylee.instance.ping"
PONG = "kaylee.instance.pong"
NO_INSTANCE_ID = '0'

# a unique (per single hosts's each browser tab or window) ID
instance.id = NO_INSTANCE_ID

instance.is_unique = (yes_callback, no_callback) ->
    PING_TIMEOUT = 1500 # ms
    pong_received = false

    #  is_unique() is called for the first time
    if instance.id == NO_INSTANCE_ID
        localStorage.clear()
        instance.id = (Math.random()).toString()
        # reply to ping requests which are coming from other tabs/windows
        # (have different instance.id)
        _storage_events_handler = (e) ->
            if e.key == PING
                localStorage[PONG] = e.newValue
            else if e.key == PONG and e.newValue == instance.id
                pong_received = true
        addEventListener('storage', _storage_events_handler, false)

    # if no "PONG" will is received in defined timeout, then
    # the current instance is considered as the only instance
    # running
    kl.log("Checking whether there are other instances of Kaylee running...")
    kl.util.after(PING_TIMEOUT, () ->
        if pong_received then no_callback() else yes_callback()
    )

    # send PING
    localStorage[PING] = instance.id
    return