
kl._test_node = () ->
    bWorker =  !!window.Worker
    if not bWorker
        return { 'feautres' : { 'worker' : false } }
    else
        return {
            features:
                worker : true
        }
