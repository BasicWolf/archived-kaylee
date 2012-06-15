pj = {}

hash_key_from_decimal_id = (dec) ->
    config = pj.config
    alphabet = config.alphabet
    len = alphabet.length;
	ret = ''
	while dec > 0
		ret = base.charAt(dec % len) + ret
		dec = Math.floor(dec / len)

    # pad with 'zeroes' if required
    if ret.length < config.key_length
        (alphabet[0] for i in [0..config.key_length - ret.length - 1 ])
	return ret


pj.init = (kl_config, app_config) ->
    importScripts("#{kl_config.lib_js_root}/md5.js")
    pj.config = app_config
    pj.get_key_by_id = (id) ->
        return cbase.to_base(id, app_config.alphabet)

    switch app_config.hash_func
        when 'md5(md5(k) + s)'
            pj.hash_func = (k, s) ->
                h = CryptoJS.algo.MD5.create()
                h.update(CryptoJS.MD5(k))
                h.update(s)
                return h.finalize().toString(CryptoJS.enc.Hex)
        when 'md5'
            pj.hash_func = (k) ->
                return CryptoJS.MD5(k)


pj.on_task_recieved = (data) ->
    task_id = data.id
    hash = data.hash_to_crack
    salt = data.salt
    key_id_start = task_id * pf.config.hashes_per_task

    for i in [0..pj.config.hashes_per_task]
        key_id = key_id_start + i
        key = hash_key_from_decimal_id(key_id)
        if hash == pj.hash_func(key, salt)
            # we have found the answer!!!