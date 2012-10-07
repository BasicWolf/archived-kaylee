###
#    klbenchmark.coffee
#    ~~~~~~~~~~~~~~~~~~
#
#    This is the base file of Kaylee client-side module.
#    It contains a benchmark executer function.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###


kl._test_node = () ->
    bWorker =  !!window.Worker
    if not bWorker
        return { 'feautres' : { 'worker' : false } }
    else
        return {
            features:
                worker : true
        }
