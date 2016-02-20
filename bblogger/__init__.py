import logging
import pprint
import traceback
import requests

HOST = 'http://localhost:5000'


class BBLogger(logging.Logger):
    def __init__(self, name):
        super(BBLogger, self).__init__(name)

        class BBHandler(logging.StreamHandler):
            def __init__(self, name):
                super(BBHandler, self).__init__()
                fmt = '%(pathname)s:%(lineno)s   %(message)s'
                self.formatter = logging.Formatter(fmt)
                self.name = name

            def emit(self, record):
                try:
                    requests.post(
                        '{0}/log/{1}'.format(HOST, self.name),
                        data={'data': self.formatter.format(record)}
                    )
                except:
                    pass

        handler = BBHandler(name)
        handler.setLevel(logging.DEBUG)
        self.addHandler(handler)
        self.name = name

    def pprint(self, thing):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, '\n' + pprint.pformat(thing), [])

    def stack(self, msg=None):
        if self.isEnabledFor(logging.INFO):
            stuff = traceback.format_stack()[:-1]
            if msg is not None:
                stuff.append(str(msg))
            else:
                stuff[-1] = stuff[-1].rstrip()
            self._log(logging.ERROR, '\n' + ''.join(stuff), [])

    def isEnabledFor(self, level):
        try:
            R = requests.get('{0}/enabled/{1}'.format(HOST, self.name))
        except:
            return False
        return level >= int(R.text)

_cache = {}


def get_logger(name):
    """
    Memoized function that constructs (or gets a pre-existing instance of)
    a logger for a given name.
    """
    if name in _cache:
        return _cache[name]
    _cache[name] = L = BBLogger(name)
    return L
