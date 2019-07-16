'''
16/07/2019
Python training day 1
'''
import logging
# logging.debug()
# report events that occur during normal operation of a program
# warnings.warn()
# logging.warning()
# issue a warning regarding a particular runtime event
# E.g. logging to a file
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')