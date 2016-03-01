import logging
from bblogger import get_logger

logger = get_logger('foo')


def start():
    pass


def stop():
    pass


def blah_blah_blah():
    pass


def do_stuff():
    get_logger('glarf').debug('This should be invisible')
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Now we are starting")
        logger.pprint(dict([
            (a, getattr(do_stuff, a)) for a in dir(do_stuff)
            if not a.startswith('__') and a != 'func_globals'
        ]))
        logger.pprint(set([1, 2, 3]))
    start()
    logger.stack()
    blah_blah_blah()
    if logger.isEnabledFor(logging.INFO):
        logger.info("Now we are stopping")
    stop()


if __name__ == '__main__':
    do_stuff()
