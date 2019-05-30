import logging


class Base:
    def __init__(self, args):
        self.setLoggerLevel(args["debug"])

    def setLoggerLevel(self, val):
        if (val == 'DEBUG'):
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def logError(self, msg):
        logging.error(msg)

    def logInfo(self, msg):
        logging.info(msg)

    def check_for_none(self, val):
        if not (val is None):
            return True
        else:
            return False

    def __del__(self):
        self.logInfo("PROCESSED XML")