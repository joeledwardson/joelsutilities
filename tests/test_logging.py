from joelsutilities import loggingutils
from queue import Queue
import logging


def test_queue_handler():
    q = Queue()
    qh = loggingutils.QueueHandler(q)
    qh.setFormatter(logging.Formatter())
    logger = logging.getLogger('testlogger')
    logger.addHandler(qh)
    logger.warning('hello')
    assert q.qsize()
    assert q.get()['txt'] == 'hello'
