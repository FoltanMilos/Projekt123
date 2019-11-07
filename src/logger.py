import logging
from colorlog import ColoredFormatter

class logger:
    global log

    def __init__(self):
        #logging.basicConfig(level=logging.DEBUG,
        #                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        #                    datefmt='%m-%d %H:%M',
        #                    #filename='/temp/myapp.log',
        #                    filemode='w')
        #console = logging.StreamHandler()
        #console.setLevel(logging.DEBUG)
        #formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        #console.setFormatter(formatter)
        #logging.getLogger('').addHandler(console)

        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        LOGFORMAT = "%(log_color)s %(asctime)s :%(levelname)-8s %(name)-12s  %(message)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger('pythonConfig')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)