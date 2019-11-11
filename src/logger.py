import logging
from colorlog import ColoredFormatter

class logger:
    global log

    def __init__(self):
        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "%(log_color)s %(asctime)s :%(levelname)-8s %(name)-12s  %(message)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger('pythonConfig')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)