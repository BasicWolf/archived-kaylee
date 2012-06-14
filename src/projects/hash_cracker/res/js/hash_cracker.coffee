pj = {}

pj.init = (kl_config, app_config) ->
    importScripts("#{kl_config.lib_js_root}/base_convert.js")
    pj.config = app_config
    pj._base_key = math.pow(pj.config.key_length
    pj.get_key_by_id = (id) ->
        return cbase.to_base(id, app_config.alphabet)

pj.on_task_recieved = (data) ->
    task_id = data.id
    hash = data.hash_to_crack
    salt = data.salt
    key_id_start = task_id * pf.config.hashes_per_task
    for i in [0..pj.config.hashes_per_task]
        hash


pj.hash_key_from_decimal_id = (dec) ->
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
