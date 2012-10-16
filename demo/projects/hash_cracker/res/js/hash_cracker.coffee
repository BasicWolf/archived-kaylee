pj.init = (kl_config, app_config) ->
    importScripts(app_config.md5_script)
    pj.config = app_config
    kl.project_imported.trigger()

pj.solve = (data) ->
    task_id = data.id
    hash = data.hash_to_crack
    salt = data.salt
    key_id_start = task_id * pj.config.hashes_per_task

    for i in [0..pj.config.hashes_per_task]
        key_id = key_id_start + i
        key = hash_key_from_decimal_id(key_id)
        klw.log("#{key}#{salt}")
        if hash == CryptoJS.MD5("#{key}#{salt}").toString(CryptoJS.enc.Hex)
            # we have found the answer!
            kl.task_completed.trigger({'key' : key})
    kl.task_completed.trigger({'__kl_result__' : false})
    return


hash_key_from_decimal_id = (dec) ->
    config = pj.config
    alphabet = config.alphabet
    len = alphabet.length;
    ret = ''
    while dec > 0
        ret = alphabet.charAt(dec % len) + ret
        dec = Math.floor(dec / len)

    # pad with 'zeroes' if required
    if ret.length < config.key_length
        (alphabet[0] for i in [0..config.key_length - ret.length - 1 ])
    return ret
