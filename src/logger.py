import logging
from colorlog import ColoredFormatter

class logger:
    global log
    global formatter

    def __init__(self):
        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "%(log_color)s %(asctime)s :%(levelname)-8s %(name)-12s  %(message)s"
        logging.root.setLevel(LOG_LEVEL)
        self.formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(self.formatter)
        self.log = logging.getLogger('pythonConfig')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)
