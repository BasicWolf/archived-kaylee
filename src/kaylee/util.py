import re
from datetime import timedelta
from .errors import KayleeError

_timeout_regex = re.compile(r'((?P<days>\d+?)d)?\s?((?P<hours>\d+?)h)?\s?'
                            '((?P<minutes>\d+?)m)?\s?((?P<seconds>\d+?)s)?')


def parse_timedelta(s):
    match = _timeout_regex.match(s)

    try:
        time_params = {}
        for (name, param) in match.groupdict().iteritems():
            if param is not None:
                time_params[name] = int(param)
        if time_params == {}:
            raise Exception()
        return timedelta(**time_params)
    except:
        raise KayleeError('Wrong timedelta string: {}'.format(s))




