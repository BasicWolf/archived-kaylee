
cbase = {}

cbase.to_base = (dec, base) ->
    len = base.length;
	ret = ''
	while dec > 0
		ret = base.charAt(dec % len) + ret
		dec = Math.floor(dec / len)
	return ret

cbase.from_base = (num, base) ->
    ret = 0
    i = 1
    while num.length > 0
        i *= base.length
		ret += base.indexOf(num.charAt(num.length - 1)) * i
		num = num.substr(0, num.length - 1);

	return ret;

cbase.convert = (val1, base1, base2) ->
    dec = cbase.from_base(val1, base1)
    return cbase.to_base(dec, base2)