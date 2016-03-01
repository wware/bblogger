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
                self.name = name

            def emit(self, record):
                data = {
                    'levelname': record.levelname,
                    'pathname': record.pathname,
                    'lineno': record.lineno,
                    'funcName': record.funcName,
                    'exc_info': record.exc_info,
                    'msg': record.msg,
                    'created': record.created
                }
                try:
                    requests.post(
                        '{0}/log/{1}'.format(HOST, self.name),
                        data=data
                    )
                except:
                    pass

        handler = BBHandler(name)
        self.addHandler(handler)

    def pprint(self, thing):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, pprint.pformat(thing), [])

    def stack(self, msg=None):
        if self.isEnabledFor(logging.INFO):
            stuff = traceback.format_stack()[:-1]
            if msg is not None:
                stuff.append(str(msg))
            else:
                stuff[-1] = stuff[-1].rstrip()
            self._log(logging.ERROR, ''.join(stuff), [])

    def isEnabledFor(self, level):
        try:
            R = requests.get('{0}/enabled/{1}'.format(HOST, self.name))
        except:
            return False
        return level >= int(R.text)


def get_logger(name, _cache={}):
    """
    Memoized function that constructs (or gets a pre-existing instance of)
    a logger for a given name.
    """
    if name not in _cache:
        _cache[name] = BBLogger(name)
    return _cache[name]
