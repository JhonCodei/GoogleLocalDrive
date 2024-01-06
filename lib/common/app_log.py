"""

@author: jalcarraz


Modification History
date-author-description

"""
__version__ = '20181113'

import logging
import sys
import os

from logging.handlers import TimedRotatingFileHandler


class _AppLogger(object):
    """docstring for _AppLogger."""

    def __init__(self):
        super(_AppLogger, self).__init__()

        self.formatter = None
        self._set_cfg_logger()

    def _set_cfg_logger(self):
        self.formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(module)s.%(funcName)s  -- %(message)s',
                              "%d.%m.%Y_%H:%M:%S")

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self, logFile):
        file_handler = TimedRotatingFileHandler(logFile)
        file_handler.setFormatter(self.formatter)
        return file_handler

    def get_logger(self, ldir, lname):

        log_cons = 'FALSE'

        if 'LOG_NAME'  in os.environ.keys(): lname    = os.environ['LOG_NAME']
        if 'LOG_DIR'   in os.environ.keys(): ldir     = os.environ['LOG_DIR' ]
        if 'LOG_CONS'  in os.environ.keys(): log_cons = os.environ['LOG_CONS']
        if 'LOG_LEVEL' in os.environ.keys(): ll = eval(f"logging.{os.environ['LOG_LEVEL']}")
        else                               : ll = logging.INFO

        logFile = os.path.join(ldir, lname)
        logger  = logging.getLogger(lname)

        logger.setLevel(ll)

        if log_cons == 'TRUE':
            logger.addHandler(self.get_console_handler())

        logger.addHandler(self.get_file_handler(logFile))

        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        print(f'In get_logger, logfile = {logFile}')
        return logger
