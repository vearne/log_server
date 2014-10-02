import logging, logging.handlers
from logging.handlers import SocketHandler
import time
logLevel=logging.INFO

logger_sms = logging.getLogger('sms')
logger = logging.getLogger('sms.sgip')

print logger_sms.parent.name
print logger.parent.name

#logger = logging.getLogger('sms.sgip')
handler = SocketHandler('localhost', 9030)
datefmt = "%Y-%m-%d %H:%M:%S"
format_str = "[%(asctime)s]: %(levelname)s %(message)s"
formatter = logging.Formatter(format_str, datefmt)
handler.setFormatter(formatter)
logger_sms.addHandler(handler)
logger.addHandler(handler)
logger.setLevel(logLevel)

logger.debug('test')
logger.info('test2------------------')

#t1 = time.time()
#for i in range(1,10000):
#    logger.info('testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest')
#
#
#t2 = time.time()

#print t2 - t1



