import logging
import os
import pprint
import requests
import foo
import bblogger
from bblogger import server
from werkzeug.wrappers import BaseRequest

here = os.path.dirname(os.path.abspath(__file__))


def test_dumb(monkeypatch):
    x = []

    def f(*args, **kwargs):
        x.append(args)
        x.append(kwargs)

    def g(url):
        class Goo(object):
            pass
        goo = Goo()
        goo.text = str(logging.INFO)
        return goo

    monkeypatch.setattr(requests, 'post', f)
    monkeypatch.setattr(requests, 'get', g)
    monkeypatch.setattr(BaseRequest, 'remote_addr', '127.0.0.1')

    assert foo
    assert bblogger
    logger = bblogger.get_logger('foo')
    l2 = bblogger.get_logger('foo')
    assert logger is l2    # test memoization

    logger.info('foo')
    assert x[0] == ('http://localhost:5000/log/foo',)
    assert x[1] == {
        'data': {
            'created': x[1]['data']['created'],
            'exc_info': None,
            'funcName': 'test_dumb',
            'levelname': 'INFO',
            'lineno': 37,
            'msg': 'foo',
            'pathname': '/home/wware/static/bblogger/tests/test_foo.py'
        }
    }

    x = []
    logger.stack('abc')
    assert x[0] == ('http://localhost:5000/log/foo',)
    assert x[1] == {
        'data': {
            'created': x[1]['data']['created'],
            'exc_info': None,
            'funcName': 'test_dumb',
            'levelname': 'ERROR',
            'lineno': 52,
            'msg': x[1]['data']['msg'],
            'pathname': '/home/wware/static/bblogger/tests/test_foo.py'
        }
    }
    assert x[1]['data']['msg'].endswith(
        'in test_dumb\n    logger.stack(\'abc\')\nabc'
    )

    assert logger.isEnabledFor(logging.DEBUG) is False
    assert logger.isEnabledFor(logging.INFO) is True

    x = []
    monkeypatch.setattr(pprint, 'pprint', f)
    assert server.enabled('foo') == ('10', 200)
    assert int(server.enabled('zoo')[0]) > logging.CRITICAL
    with server.app.test_request_context() as RC:
        RC.request.form = {'data': 'abcd'}
        assert server.post('foo') == ('', 200)
        assert server.post('zoo') == ('', 200)
    assert x == [({'data': 'abcd'},), {}, ({'data': 'abcd'},), {}]
