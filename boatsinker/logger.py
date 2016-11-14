# Simple logger std out logger

class Logger(object):
    DEBUG = 4
    INFO = 3
    WARN = 2
    ERROR = 1
    SILENT = 0

    __instance = None
    
    def __new__(cls, loglevel=None):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
            if loglevel is None:
                Logger.__instance.loglevel = Logger.INFO
            else:
                Logger.__instance.loglevel = loglevel
        return Logger.__instance

    def debug(self, msg):
        if self.loglevel >= self.DEBUG:
            print('Debug: {0}'.format(msg))

    def info(self, msg):
        if self.loglevel >= self.INFO:
            print('Info: {0}'.format(msg))

    def warn(self, msg):
        if self.loglevel >= self.WARN:
            print('Warn: {0}'.format(msg))

    def error(self, msg):
        if self.loglevel >= self.ERROR:
            print('Error: {0}'.format(msg))

